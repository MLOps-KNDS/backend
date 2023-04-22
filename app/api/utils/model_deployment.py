import logging
from kubernetes import client, config

_logger = logging.getLogger(__name__)


class ModelDeployment:
    def __init__(
        self,
        image_tag: str,
        replicas: int,
        cpu_limit: int,
        cpu_request: int,
        memory_limit: int,
        memory_request: int,
    ) -> None:
        self.image_tag: str = image_tag
        self.replicas: int = replicas
        self.cpu_limit: int = cpu_limit
        self.cpu_request: int = cpu_request
        self.memory_limit: int = memory_limit
        self.memory_request: int = memory_request
        self.pod_created = False
        self.service_created = False

    def deploy(self):
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
        v1 = client.CoreV1Api()
        deployment = self.__create_deployment()
        res = v1.create_namespaced_deployment(namespace="default", body=deployment)

    def __create_deployment(self):
        metadata = client.V1ObjectMeta(name=self.image_tag)
        containers = client.V1Container(name="model-test", image=self.image_tag)
        pod_spec = client.V1PodSpec(containers=containers)
        pod_template_spec = client.V1PodTemplateSpec(spec=pod_spec)
        deployment_spec = client.V1DeploymentSpec(
            replicas=self.replicas, template=pod_template_spec
        )
        deployment = client.V1Pod(
            metadata=metadata, spec=deployment_spec, kind="Deployment"
        )
        return deployment
