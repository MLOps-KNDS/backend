import logging
from kubernetes import client, config
from kubernetes.client import V1PodList
import time
from typing import Callable
from enum import Enum

_logger = logging.getLogger(__name__)


# Pod phases
class PodPhase(str, Enum):
    """
    Class to store pod phases
    """

    PENDING = "Pending"
    RUNNING = "Running"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    UNKNOWN = "Unknown"


class Pinger:
    """
    Pings resource using kubernetes api.
    """

    def __init__(
        self,
        ping_callback: Callable,
        ping_callback_args: dict,
        predicate: Callable,
        error_callback: Callable,
        error_callback_args: dict,
        ping_amount: int,
    ) -> None:
        config.load_incluster_config()

        self.ping_callback = ping_callback
        self.ping_callback_args = ping_callback_args
        self.predicate = predicate
        self.error_callback = error_callback
        self.error_callback_args = error_callback_args
        self.ping_amount = ping_amount

    def ping(self) -> bool:
        """
        Pings a resource and logs every action.
        Uses callback functions to ping and check if the resource is responding.
        In case of failure or no response uses callback function to log the error
        and do something about it.

        :return: True if the resource responds, false otherwise
        """
        _logger.info("Pinging resource...")
        for i in range(1, self.ping_amount + 1):
            _logger.info(f"Pinging resource {i}/{self.ping_amount}...")
            api_response = self.ping_callback(**self.ping_callback_args)
            if self.predicate(api_response):
                _logger.info("Resource responded!")
                return True
            _logger.info(f"Resource is not responding waiting for {5 * i} seconds...")
            time.sleep(5 * i)
        _logger.error("Resource didn't respond in given time!")
        self.error_callback(**self.error_callback_args, api_response=api_response)
        return False

    @classmethod
    def deployment_ping(cls, name: str, namespace: str) -> V1PodList:
        """
        Returns a list of pods for a given deployment

        :param name: Name of the deployment
        :param namespace: Namespace of the deployment
        :return: List of pods
        """
        v1 = client.CoreV1Api()
        return v1.list_namespaced_pod(namespace=namespace, label_selector=f"app={name}")

    @classmethod
    def deployment_predicate(cls, api_response: V1PodList) -> bool:
        """
        Checks if all pods are running

        :param api_response: Response from kubernetes api
        :return: True if all pods are running, false otherwise
        """
        # Check if everypod is running. List assumed to be not empty
        for pod in api_response.items:
            if pod.status.phase != "Running":
                return False
        return True

    @classmethod
    def deployment_error_callback(
        cls, name: str, namespace: str, api_response: V1PodList
    ):
        """
        Deletes a deployment and logs why the deployment failed

        :param name: Name of the deployment
        :param namespace: Namespace of the deployment
        """
        finished = False
        v1 = client.AppsV1Api()
        for pod in api_response.items:
            _logger.error(
                f"Pod {pod.metadata.name} in namespace {namespace} is in state "
                f"{pod.status.phase}."
            )
            for condition in pod.status.conditions:
                if condition.type == "PodScheduled" and condition.status == "False":
                    _logger.error(
                        "Pod is not scheduled. \n"
                        f"Reason: {condition.reason}. Message: {condition.message}"
                    )
                    finished = True
            if finished:
                break
            {
                PodPhase.PENDING: lambda: _logger.error(
                    f"Reason: {pod.status.container_statuses[0].state.waiting.reason}. "
                    f"Message: {pod.status.container_statuses[0].state.waiting.message}"
                ),
                PodPhase.FAILED: lambda: _logger.error(
                    "Reason: "
                    f"{pod.status.container_statuses[0].state.terminated.reason}. "
                    "Message: "
                    f"{pod.status.container_statuses[0].state.terminated.message}."
                ),
            }.get(
                pod.status.phase, lambda: _logger.error("Could not match pod's phase")
            )()

        _logger.error(f"Deleting deployment {name} in namespace {namespace}...")
        try:
            v1.delete_namespaced_deployment(name=name, namespace=namespace)
        except Exception as e:
            _logger.error(f"Deleting deployment {name} in namespace {namespace} failed")
            raise e
        else:
            _logger.error(
                f"Deleting deployment {name} in namespace {namespace} finished"
            )
