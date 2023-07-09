import logging
from kubernetes import client, config
from kubernetes.client import V1PodList
import time
from typing import Callable

from utils.exception import PingLimitReached, ErrImagePull, EmptyList, ErrImageNeverPull

_logger = logging.getLogger(__name__)


# Pod phases
class PodPhase:
    """
    Class to store pod phases
    """

    PENDING = "Pending"
    RUNNING = "Running"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    UNKNOWN = "Unknown"


# Container states
class ContainerState:
    """
    Class to store container states
    """

    WAITING = "Waiting"
    RUNNING = "Running"
    SUCCEEDED = "Succeeded"


class Exceptions:
    """
    Class to store exceptions
    """

    ERR_IMAGE_PULL = "ErrImagePull"
    ERR_IMAGE_NEVER_PULL = "ErrImageNeverPull"


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

        :return: True if the resource is ready, false if resource
        doesn't exist

        :raises: PingLimitReached if the resource is not ready in given time
        """
        _logger.info("Pinging resource...")
        for i in range(self.ping_amount):
            _logger.info(f"Pinging resource {i+1}/{self.ping_amount}...")
            api_response = self.ping_callback(**self.ping_callback_args)
            try:
                if self.predicate(api_response):
                    _logger.info("Service responded!")
                    return True
            except EmptyList as e:
                _logger.error(f"Pinging resource returned empty list: {e}")
                return False
            except ErrImagePull as e:
                _logger.error(f"Error while pinging resource: {e}")
                self.error_callback(
                    **self.error_callback_args, api_response=api_response
                )
                raise e
            _logger.info(f"Serivce is not ready yet waiting for {5 * i} seconds...")
            time.sleep(5 * i)
        _logger.error("Service didn't respond in given time!")
        self.error_callback(**self.error_callback_args, api_response=api_response)
        raise PingLimitReached(
            self.ping_amount,
            "Service didn't respond in given time!",
        )

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
        if len(api_response.items) == 0:
            raise EmptyList("Empty list")
        # Check if everypod is running
        for pod in api_response.items:
            if pod.status.phase == "Pending":
                # Error list should be expanded
                if (
                    pod.status.container_statuses[0].state.waiting.reason
                    == "ErrImagePull"
                ):
                    raise ErrImagePull(
                        pod.status.container_statuses[0].image,
                        "Image pull error: "
                        f"{pod.status.container_statuses[0].state.waiting.message}",
                    )
                if (
                    pod.status.container_statuses[0].state.waiting.reason
                    == "ErrImageNeverPull"
                ):
                    raise ErrImageNeverPull(
                        pod.status.container_statuses[0].image,
                        "Image never pull error: "
                        f"{pod.status.container_statuses[0].state.waiting.message}. "
                        "Checkout imagePullPolicy or image tag!",
                    )

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
        v1 = client.AppsV1Api()
        for pod in api_response.items:
            _logger.error(
                f"Pod {pod.metadata.name} in namespace {namespace} is in state "
                f"{pod.status.phase}."
            )

            {
                PodPhase.PENDING: lambda: _logger.error(
                    f"Reason {pod.status.container_statuses[0].state.waiting.reason}. "
                    f"Message {pod.status.container_statuses[0].state.waiting.message}"
                ),
                PodPhase.FAILED: lambda: _logger.error(
                    "Reason "
                    f"{pod.status.container_statuses[0].state.terminated.reason}. "
                    "Message "
                    f"{pod.status.container_statuses[0].state.terminated.message}"
                ),
            }.get(pod.status.phase, lambda: None)()

        _logger.error(f"Deleting deployment {name} in namespace {namespace}...")
        v1.delete_namespaced_deployment(name=name, namespace=namespace)
        _logger.error(f"Deleting deployment {name} in namespace {namespace} finished")
