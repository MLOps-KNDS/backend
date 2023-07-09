import logging
from kubernetes import client, config
from kubernetes.client import V1PodList
import time

from utils.exception import PingLimitReached, ErrImagePull, EmptyList

_logger = logging.getLogger(__name__)


class Pinger:
    """
    Pings services in a given namespace using kubernetes api.
    """

    def __init__(
        self,
        name: str,
        namespace: str,
        ping_callback: callable[str, str],
        predicate: callable[str],
        error_callback: callable[str, str],
        ping_amount: int,
    ) -> None:
        config.load_incluster_config()

        self.name = name  # Assumed to be already with prefix (e.g. "tyro-model-")
        self.namespace = namespace
        self.ping_callback = ping_callback
        self.predicate = predicate
        self.error_callback = error_callback
        self.ping_amount = ping_amount

    def ping(self) -> bool:
        """
        Pings a service and logs every action.

        :return: True if the service is ready, false if service
        doesn't exist

        :raises: PingLimitReached if the service is not ready in given time
        """
        _logger.info(f"Pinging service {self.name} in namespace {self.namespace}...")
        for i in range(self.ping_amount):
            _logger.info(
                f"Pinging service {self.name} in namespace {self.namespace} "
                f"{i+1}/{self.ping_amount}..."
            )
            api_response = self.ping_callback(name=self.name, namespace=self.namespace)
            try:
                if self.predicate(api_response):
                    _logger.info(f"{self.name} in namespace {self.namespace} is ready!")
                    return True
            except EmptyList as e:
                _logger.error(
                    f"Pinging {self.name} in namespace {self.namespace} returned "
                    f"empty list: {e}"
                )
                return False
            except ErrImagePull as e:
                _logger.error(
                    f"Error while pinging {self.name} in namespace {self.namespace}: "
                    f"{e}"
                )
                self.error_callback(self.name, self.namespace, api_response)
                raise e
            _logger.info(
                f"{self.name} in namespace {self.namespace} is not ready yet"
                f" waiting for {1*i} seconds..."
            )
            time.sleep(5 * i)
        _logger.error(
            f"{self.name} in namespace {self.namespace} didn't respond in given time!"
        )
        self.error_callback(self.name, self.namespace, api_response)
        raise PingLimitReached(
            self.ping_amount,
            f"{self.name} in namespace {self.namespace} didn't respond in given time!",
        )

    @classmethod
    def deployment_ping(cls, name: str, namespace: str) -> V1PodList:
        """
        Returns a list of pods for a given deployment

        :param name: Name of the deployment
        :param namespace: Namespace of the deployment
        :return: List of pods
        """
        config.load_incluster_config()
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
            if pod.status.phase == "Pending":
                _logger.error(
                    f"Reason {pod.status.container_statuses[0].state.waiting.reason}. "
                    f"Message {pod.status.container_statuses[0].state.waiting.message}"
                )
            if pod.status.phase == "Failed":
                _logger.error(
                    "Reason "
                    f"{pod.status.container_statuses[0].state.terminated.reason}. "
                    "Message "
                    f"{pod.status.container_statuses[0].state.terminated.message}"
                )

        _logger.error(f"Deleting deployment {name} in namespace {namespace}...")
        v1.delete_namespaced_deployment(name=name, namespace=namespace)
        _logger.error(f"Deleting deployment {name} in namespace {namespace} finished")
