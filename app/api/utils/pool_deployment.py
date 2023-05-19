from kubernetes import client, config
from schemas import model as model_schemas
from istio_manifest_generator import IstioVirtualServiceGenerator
from constants import Constants


class PoolDeployment:
    """
    Creates virtual service for a pool of models
    """

    def __init__(self, models: list[model_schemas.Model], pool_name: str) -> None:
        """
        :param models: list of models to which the user will be redirected to
        :param pool_name: name of the pool
        """

        self.models = models
        self.name = pool_name

        config.load_incluster_config()

    def deploy(self):
        custom_api = client.CustomObjectsApi()

        body = IstioVirtualServiceGenerator(self.models, self.name)
        body = body.generate()

        custom_api.create_namespaced_custom_object(
            group=Constants.ISTIO_VS_GROUP,
            version=Constants.ISTIO_VS_VERSION,
            namespace=self.name,
            plural="virtualservices",
            body=body,
        )
