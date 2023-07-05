import logging
from kubernetes import client, config
import time

from utils.constants import Constants
from models import ModelDetails
from config.exceptions import PingLimitReached

_logger = logging.getLogger(__name__)


class ModelDeployment:
    """
    Deploys a docker image to a kubernetes cluster.
    Creates deployment and service attached to it.
    """

    def __init__(
        self,
        name: str,
        model_details: ModelDetails,
    ) -> None:
        """
        :param name: Name of the deployment and service. Must be unique
        :param model_details: Model details
        """
        self.name: str = name
        self.image_tag: str = model_details.image_tag
        self.replicas: int = model_details.replicas
        self.cpu_limit: str = model_details.cpu_limit
        self.cpu_request: str = model_details.cpu_request
        self.memory_limit: str = model_details.memory_limit
        self.memory_request: str = model_details.memory_request

        config.load_incluster_config()

    def deploy(self) -> None:
        """
        Deploys a docker image to a kubernetes cluster.

        :raises: Any exception which may occur
        """
        try:
            _logger.info(f"Deploying a docker image with tag {self.image_tag}...")
            self.__deploy_to_k8s()
            _logger.info(f"Deploying a docker image with tag {self.image_tag} finished")
        except Exception as e:
            _logger.error(
                f"Deploying an image with tag {self.image_tag} failed with error: {e}"
            )
            raise e

    def __deploy_to_k8s(self) -> None:
        v1_apps = client.AppsV1Api()
        _logger.info(f"Creating deployment with name: {self.name}...")
        try:
            deployment = self.__create_deployment()
            v1_apps.create_namespaced_deployment(
                namespace=Constants.K8S_NAMESPACE_MODELS, body=deployment
            )
            max_checks = 10
            num_checks = 0

            # Check deployment status
            while num_checks < max_checks:
                deployment_status = v1_apps.read_namespaced_deployment_status(
                    name=self.name,
                    namespace=Constants.K8S_NAMESPACE_MODELS,
                )
                _logger.info(
                    f"Ping status for deployment with name {self.name}: "
                    "{deployment_status.status.ready_replicas}"
                    "/{deployment_status.status.replicas}"
                )
                if (
                    deployment_status.status.ready_replicas
                    == deployment_status.status.replicas
                ):
                    _logger.info(f"Deployment with name {self.name} created!")
                    break
                num_checks += 1
                _logger.info(
                    f"Waiting for {2*num_checks} seconds for deployment with "
                    "name {self.name} to be created..."
                )
                time.sleep(2 * num_checks)
            if num_checks == max_checks:
                raise PingLimitReached(
                    f"Deployment with name {self.name} not created in time!"
                )
        except Exception as e:
            _logger.error(
                f"Creation of deployment with name: {self.name} failed with error: {e}!"
                "\nAborting process!"
            )
            raise e

        v1_core = client.CoreV1Api()
        _logger.info(f"Creating service with name: {self.name}...")
        try:
            service = self.__create_service()
            v1_core.create_namespaced_service(
                namespace=Constants.K8S_NAMESPACE_MODELS, body=service
            )
            max_checks = 10
            num_checks = 0

            # Check service status
            while num_checks < max_checks:
                service_status = v1_core.read_namespaced_service_status(
                    name=self.name,
                    namespace=Constants.K8S_NAMESPACE_MODELS,
                )
                if not service_status.status.load_balancer:
                    _logger.info(f"Service with name {self.name} created!")
                    break
                num_checks += 1
                _logger.info(
                    f"Waiting for {2*num_checks} seconds for service with "
                    "name {self.name} to be created..."
                )
                time.sleep(2 * num_checks)
            if num_checks == max_checks:
                raise PingLimitReached(
                    f"Service with name {self.name} not created in time!"
                )
        except Exception as e:
            _logger.error(
                f"Creation of service with name: {self.name} failed with error: {e}!"
                "\nAborting process!"
            )
            v1_apps.delete_namespaced_deployment(
                name=self.name, namespace=Constants.K8S_NAMESPACE_MODELS
            )
            raise e
        else:
            _logger.info(f"Service with name {self.name} created!")

    def __create_deployment(self) -> client.V1Deployment:
        container = client.V1Container(
            name=self.name,
            image=self.image_tag,
            ports=[
                client.V1ContainerPort(container_port=Constants.K8S_DEPLOYMENT_PORT)
            ],
            resources=client.V1ResourceRequirements(
                requests={"cpu": self.cpu_request, "memory": self.memory_request},
                limits={"cpu": self.cpu_limit, "memory": self.memory_limit},
            ),
        )

        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"model": self.name}),
            spec=client.V1PodSpec(containers=[container]),
        )

        spec = client.V1DeploymentSpec(
            replicas=self.replicas,
            template=template,
            selector=client.V1LabelSelector(match_labels={"model": self.name}),
        )

        deployment = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name=self.name),
            spec=spec,
        )
        return deployment

    def __create_service(self) -> client.V1Service:
        port = client.V1ServicePort(
            protocol="TCP",
            port=Constants.K8S_SERVICE_PORT,
            target_port=Constants.K8S_DEPLOYMENT_PORT,
        )

        spec = client.V1ServiceSpec(
            selector={"model": self.name},
            ports=[port],
        )

        service = client.V1Service(
            api_version="v1",
            kind="Service",
            metadata=client.V1ObjectMeta(name=self.name),
            spec=spec,
        )
        return service

    @classmethod
    def delete(cls, name: str) -> None:
        """
        Deletes deployment and service with a given name.

        :raises: Any exception which may occur
        :param name: Name of the deployment and service
        """
        v1_apps = client.AppsV1Api()
        try:
            _logger.info(f"Deleteing deployment with name {name}...")
            v1_apps.delete_namespaced_deployment(
                name=name, namespace=Constants.K8S_NAMESPACE_MODELS
            )
            _logger.info(f"Deleteing deployment with name {name} finished.")
        except Exception as e:
            _logger.error(
                f"Deleteing deployment with name {name} failed with error: {e}"
            )
            raise e

        v1_core = client.CoreV1Api()
        try:
            _logger.info(f"Deleteing service with name {name}...")
            v1_core.delete_namespaced_service(
                name=name, namespace=Constants.K8S_NAMESPACE_MODELS
            )
            _logger.info(f"Deleteing service with name {name} finished.")
        except Exception as e:
            _logger.error(f"Deleteing service with name {name} failed with error: {e}")
            raise

        # Wait for deployment and service deletion
        max_checks = 10
        num_checks = 0

        while num_checks < max_checks:
            try:
                # Check if deployment exists
                v1_apps.read_namespaced_deployment(
                    name=name, namespace=Constants.K8S_NAMESPACE_MODELS
                )
            except client.exceptions.ApiException as e:
                if e.status == 404:
                    deployment_deleted = True
                else:
                    raise
            else:
                deployment_deleted = False

            try:
                # Check if service exists
                v1_core.read_namespaced_service(
                    name=name, namespace=Constants.K8S_NAMESPACE_MODELS
                )
            except client.exceptions.ApiException as e:
                if e.status == 404:
                    service_deleted = True
                else:
                    raise
            else:
                service_deleted = False

            if deployment_deleted and service_deleted:
                _logger.info(
                    f"Deployment and service with name {name} deleted successfully!"
                )
                return

            num_checks += 1
            _logger.info(
                f"Waiting for {5*num_checks} seconds for deployment and service with "
                f"name {name} to be deleted..."
            )
            time.sleep(5 * num_checks)
        if num_checks == max_checks:
            raise PingLimitReached(
                f"Deployment and service with name {name} not deleted in time!"
            )
