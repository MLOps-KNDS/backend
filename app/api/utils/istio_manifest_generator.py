from schemas import model as model_schemas
from .constants import Constants


class IstioVirtualServiceGenerator:
    def __init__(self, models: list[model_schemas.Model], pool_name: str):
        """
        :param models: list of models to which the user will be redirected to
        :param pool_name: name of the pool
        """
        self.models = models
        self.name = pool_name

    def generate(self) -> dict:
        """
        :return: Istio Virtual Service manifest
        """
        body = {
            "apiVersion": f"{Constants.ISTIO_VS_GROUP}/{Constants.ISTIO_VS_VERSION}",
            "kind": "VirtualService",
            "metadata": {"name": self.pool_name},
            "spec": {
                "hosts": ["*"],
                "http": [
                    {
                        "route": [
                            {
                                "destination": {
                                    "host": model.name,
                                    "port": {"number": Constants.K8S_SERVICE_PORT},
                                }
                            }
                            for model in self.models
                        ]
                    }
                ],
            },
        }
        return body
