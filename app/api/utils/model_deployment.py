import logging
from kubernetes import client, config
import time

from utils.constants import Constants
from utils.cluster_pingers import Pinger
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
        self.name: str = Constants.K8S_MODEL_PREFIX + name
        self.image_tag: str = model_details.image_tag
        self.min_replicas: int = model_details.min_replicas
        self.max_replicas: int = model_details.max_replicas
        self.cpu_limit: str = model_details.cpu_limit
        self.cpu_request: str = model_details.cpu_request
        self.cpu_utilization: int = model_details.cpu_utilization
        self.memory_limit: str = model_details.memory_limit
        self.memory_request: str = model_details.memory_request
        self.memory_utilization: int = model_details.memory_utilization

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
        hpa = self.__create_horizontal_pod_autoscaler()
        service = self.__create_service()
        v1.create_namespaced_deployment(
            namespace=Constants.K8S_NAMESPACE_MODELS, body=deployment
        )
        time.sleep(5)
        args = {"name": self.name, "namespace": Constants.K8S_NAMESPACE_MODELS}
        deployment_pinger = Pinger(
            Pinger.deployment_ping,
            args,
            Pinger.deployment_predicate,
            Pinger.deployment_error_callback,
            args,
            Constants.K8S_PING_LIMIT,
        )
        if not deployment_pinger.ping():
            raise Exception(
                f"Deployment with name {self.name} didn't respond in given time!"
            )
        _logger.info(f"Deployment with name {self.name} ready")
        v1 = client.CoreV1Api()
        v1.create_namespaced_service(
            namespace=Constants.K8S_NAMESPACE_MODELS, body=service
        )
        _logger.info(f"Service with name {self.name} ready")
        if hpa is not None:
            _logger.info(f"Creating horizontal pod autoscaler for {self.name}...")
            v2 = client.AutoscalingV2Api()
            v2.create_namespaced_horizontal_pod_autoscaler(
                namespace=Constants.K8S_NAMESPACE_MODELS, body=hpa
            )
            _logger.info(f"Creating horizontal pod autoscaler for {self.name} finished")
        else:
            _logger.info(f"Skipping horizontal pod autoscaler for {self.name}")

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
            metadata=client.V1ObjectMeta(labels={"app": self.name}),
            spec=client.V1PodSpec(containers=[container]),
        )

        spec = client.V1DeploymentSpec(
            replicas=self.min_replicas,
            template=template,
            selector=client.V1LabelSelector(match_labels={"app": self.name}),
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
            selector={"app": self.name},
            ports=[port],
        )

        service = client.V1Service(
            api_version="v1",
            kind="Service",
            metadata=client.V1ObjectMeta(name=self.name),
            spec=spec,
        )
        return service

    def __create_horizontal_pod_autoscaler(
        self,
    ) -> client.V2HorizontalPodAutoscaler | None:
        metadata = client.V1ObjectMeta(name=self.name)

        metrics = self.__create_metrics()

        if len(metrics) == 0:
            _logger.info("No metrics specified, skipping autoscaling")
            return None

        spec = client.V2HorizontalPodAutoscalerSpec(
            max_replicas=self.max_replicas,
            min_replicas=self.min_replicas,
            scale_target_ref=client.V1CrossVersionObjectReference(
                api_version="apps/v1",
                kind="Deployment",
                name=self.name,
            ),
            metrics=metrics,
        )

        hpa = client.V2HorizontalPodAutoscaler(
            kind="HorizontalPodAutoscaler",
            metadata=metadata,
            spec=spec,
        )

        return hpa

    def __create_metrics(self):
        _logger.debug(f"Creating metrics for {self.name}...")
        metrics = []
        if self.cpu_utilization:
            _logger.debug(f"Creating cpu utilization metric for {self.name}")
            metrics.append(
                client.V2MetricSpec(
                    type="Resource",
                    resource=client.V2ResourceMetricSource(
                        name="cpu",
                        target=client.V2MetricTarget(
                            type="Utilization",
                            average_utilization=self.cpu_utilization,
                        ),
                    ),
                ),
            )
        if self.memory_utilization:
            _logger.debug(f"Creating memory utilization metric for {self.name}")
            metrics.append(
                client.V2MetricSpec(
                    type="Resource",
                    resource=client.V2ResourceMetricSource(
                        name="memory",
                        target=client.V2MetricTarget(
                            type="Utilization",
                            average_utilization=self.memory_utilization,
                        ),
                    ),
                ),
            )
        return metrics

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

        v2 = client.AutoscalingV2Api()
        try:
            v2.read_namespaced_horizontal_pod_autoscaler(
                name=name, namespace=Constants.K8S_NAMESPACE_MODELS
            )
        except Exception:
            _logger.info(
                f"Horizontal pod autoscaler with name {name} not found, "
                "skipping deletion"
            )
            return
        try:
            _logger.info(f"Deleteing horizontal pod autoscaler with name {name}...")
            v2.delete_namespaced_horizontal_pod_autoscaler(
                name=name, namespace=Constants.K8S_NAMESPACE_MODELS
            )
            _logger.info(
                f"Deleteing horizontal pod autoscaler with name {name} finished."
            )
        except Exception as e:
            _logger.error(
                f"Deleteing horizontal pod autoscaler with name {name} "
                f"failed with error: {e}"
            )
            raise
