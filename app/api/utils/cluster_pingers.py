import logging
from kubernetes import client
import requests
import time

from config.exceptions import PingLimitReached

_logger = logging.getLogger(__name__)


class DeploymentPing:
    @classmethod
    def ping(cls, deployment_name: str, deployment_namespace: str) -> bool:
        v1_apps = client.AppsV1Api()
        try:
            max_checks = 10
            num_checks = 0

            # Check deployment status
            while num_checks < max_checks:
                deployment_status = v1_apps.read_namespaced_deployment_status(
                    name=deployment_name,
                    namespace=deployment_namespace,
                )
                _logger.info(
                    f"Ping status for deployment with name {deployment_name}: "
                    f"{deployment_status.status.ready_replicas}"
                    f"/{deployment_status.status.replicas}"
                )
                if (
                    deployment_status.status.ready_replicas
                    == deployment_status.status.replicas
                ):
                    _logger.info(f"Deployment with name {deployment_name} responded!")
                    return True
                num_checks += 1
                _logger.info(
                    f"Waiting for {2*num_checks} seconds for deployment with "
                    f"name {deployment_name} to respond..."
                )
                time.sleep(2 * num_checks)
            if num_checks == max_checks:
                raise PingLimitReached(
                    f"Deployment with name {deployment_name} didn't respond in time!"
                )
        except Exception as e:
            _logger.error(
                f"Pinging of deployment with name: {deployment_name} failed "
                f"with error: {e}!"
            )
            raise e

        return False


class ServicePing:
    @classmethod
    def ping(cls, service_name: str, service_namespace: str):
        v1_core = client.CoreV1Api()
        try:
            max_checks = 10
            num_checks = 0

            service = v1_core.read_namespaced_service(
                name=service_name, namespace=service_namespace
            )
            service_endpoint = service.spec.cluster_ip
            service_port = service.spec.ports[0].port
            # Construct the service URL
            service_url = f"http://{service_endpoint}:{service_port}"

            # Check service status
            while num_checks < max_checks:
                # Perform an HTTP GET request to the service endpoint
                response = requests.get(service_url)
                # Check the response status code
                if response.status_code == 200:
                    return True
                num_checks += 1
                _logger.info(
                    f"Waiting for {2*num_checks} seconds for service with "
                    f"name {service_name} to respond..."
                )
                time.sleep(2 * num_checks)

        except Exception as e:
            _logger.error(
                f"Pinging of service with name: {service_name} failed "
                f"with error: {e}!"
            )
            raise e
        return False
