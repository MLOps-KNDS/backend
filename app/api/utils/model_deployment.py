import logging
from kubernetes import client, config

_logger = logging.getLogger(__name__)

config.load_incluster_config()


class ModelDeployment:
    """
    Deploys a docker image to a kubernetes cluster.
    Creates deployment and service attached to it.
    """

    def __init__(
        self,
        name: str,
        image_tag: str,
        replicas: int,
        cpu_limit: str,
        cpu_request: str,
        memory_limit: str,
        memory_request: str,
    ) -> None:
        """
        :param name: Name of the deployment and service. Must be unique
        :param image_tag: Tag to docker images
        :param replicas: Number of pod replicas per deployment
        :param cpu_limit: Maximum cpu usage
        :param cpu_request: Requested cpu amount
        :param memory_limit: Maximum memory usage
        :param memory_request: Requested memory amount
        """
        self.name: str = name
        self.image_tag: str = image_tag
        self.replicas: int = replicas
        self.cpu_limit: str = cpu_limit
        self.cpu_request: str = cpu_request
        self.memory_limit: str = memory_limit
        self.memory_request: str = memory_request

    def deploy(self):
        """
        Deploys a docker image to a kubernetes cluster.
        """

        try:
            _logger.info(f"Deploying a docker image with tag {self.image_tag}...")
            self.__deploy_to_k8s()
            _logger.info(f"Deploying a docker image with tag {self.image_tag} finished")
        except Exception as e:
            _logger.error(
                f"Deploying a docker image with tag {self.image_tag} failed with error: {e}"
            )
            raise e

    def __deploy_to_k8s(self):
        v1 = client.AppsV1Api()
        deployment = self.__create_deployment()
        service = self.__create_service()
        deploy_result = v1.create_namespaced_deployment(
            namespace="default", body=deployment
        )
        v1 = client.CoreV1Api()
        service_result = v1.create_namespaced_service(namespace="default", body=service)

    def __create_deployment(self):

        container = client.V1Container(
            name=self.name,
            image=self.image_tag,
            ports=[client.V1ContainerPort(container_port=80)],
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

    def __create_service(self):

        port = client.V1ServicePort(protocol="TCP", port=8001, target_port=80)

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
