from kubernetes import client, config
from schemas import pool as pool_schemas
from .istio_manifest_generator import IstioGatewayGenerator


class GatewayDeployment:
    """
    Creates gateway for a our gate
    """

    def __init__(self, pools: list[pool_schemas.Pool], gateway_name: str) -> None:
        """
        :param gateway_name: name of the gateway
        """

        self.name = gateway_name
        self.pools = pools

        config.load_incluster_config()

    def deploy(self):
        custom_api = client.CustomObjectsApi()

        body = IstioGatewayGenerator(self.name, self.pools)
        body = body.generate()

        custom_api.create_namespaced_custom_object(
            group="networking.istio.io/v1alpha3",
            version="v1alpha3",
            namespace=f"gateway-config-{self.name}",
            plural="gateways",
            body=body,
        )
