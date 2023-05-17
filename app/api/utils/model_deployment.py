import logging
from kubernetes import client, config

from utils.constants import Constants
from models import ModelDetails

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
        v1 = client.AppsV1Api()
        deployment = self.__create_deployment()
        service = self.__create_service()
        v1.create_namespaced_deployment(
            namespace=Constants.K8S_NAMESPACE_MODELS, body=deployment
        )
        _logger.info(f"Deployment with name {self.name} ready")
        v1 = client.CoreV1Api()
        v1.create_namespaced_service(
            namespace=Constants.K8S_NAMESPACE_MODELS, body=service
        )
        _logger.info(f"Service with name {self.name} ready")

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
        v1 = client.AppsV1Api()
        try:
            _logger.info(f"Deleteing deployment with name {name}...")
            v1.delete_namespaced_deployment(
                name=name, namespace=Constants.K8S_NAMESPACE_MODELS
            )
            _logger.info(f"Deleteing deployment with name {name} finished.")
        except Exception as e:
            _logger.error(
                f"Deleteing deployment with name {name} failed with error: {e}"
            )
            raise e

        v1 = client.CoreV1Api()
        try:
            _logger.info(f"Deleteing service with name {name}...")
            v1.delete_namespaced_service(
                name=name, namespace=Constants.K8S_NAMESPACE_MODELS
            )
            _logger.info(f"Deleteing service with name {name} finished.")
        except Exception as e:
            _logger.error(f"Deleteing service with name {name} failed with error: {e}")
            raise
