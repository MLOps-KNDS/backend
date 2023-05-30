from kubernetes import client, config
from schemas import pool_model as pool_model_schemas
from .istio_manifest_generator import IstioVirtualServiceGenerator


class PoolDeployment:
    """
    Creates virtual service for a pool of models
    """

    def __init__(
        self,
        pool_models: list[pool_model_schemas.PoolModelDetailed],
        pool_name: str,
        gatewaway_name: str,
    ) -> None:
        """
        :param models: list of models to which the user will be redirected to
        :param pool_name: name of the pool
        """

        self.pool_models = pool_models
        self.gatewaway_name = gatewaway_name
        self.name = pool_name

        config.load_incluster_config()

    def deploy(self):
        custom_api = client.CustomObjectsApi()

        body = IstioVirtualServiceGenerator(
            self.pool_models, self.name, self.gatewaway_name
        )
        body = body.generate()

        custom_api.create_namespaced_custom_object(
            group="networking.istio.io/v1alpha3",
            version="v1alpha3",
            namespace=f"pool-config-{self.name}",
            plural="virtualservices",
            body=body,
        )