from kubernetes import client, config
from .istio_manifest_generator import IstioGatewayGenerator
from .constants import Constants


class GatewayDeployment:
    """
    Creates gateway for a our gate
    """

    def __init__(self, gateway_name: str, pool_names: list[str]) -> None:
        """
        :param gateway_name: name of the gateway
        :param pool_names: list of pools to which the user will be redirected to
        """

        self.gateway_name = gateway_name
        self.pool_names = pool_names

        config.load_incluster_config()

    def deploy(self):
        custom_api = client.CustomObjectsApi()

        body = IstioGatewayGenerator(self.gateway_name, self.pool_names)
        body = body.generate()

        custom_api.create_namespaced_custom_object(
            group="networking.istio.io/v1alpha3",
            version="v1alpha3",
            namespace=Constants.K8S_NAMESPACE_MODELS,
            plural="gateway",
            body=body,
        )
