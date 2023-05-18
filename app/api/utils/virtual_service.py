from kubernetes import client, config
from schemas import model as model_schemas
from istio_manifest_generator import IstioManifestGen
from constants import Constants


class VirtualService:
    """
    Creates virtual service for a pool of models
    """

    def __init__(self, models: list[model_schemas.Model], pool_name: str) -> None:
        """
        :param models: list of models to which the user will be redirected
        :param pool_name: name of the pool
        """

        self.models = models
        self.name = pool_name

        config.load_incluster_config()

    def deploy(self):
        custom_api = client.CustomObjectsApi()

        body = IstioManifestGen.generate_vs_manifest(self.models, self.name)

        custom_api.create_namespaced_custom_object(
            group=Constants.GROUP,
            version=Constants.VERSION,
            namespace=self.name,
            plural="virtualservices",
            body=body,
        )
