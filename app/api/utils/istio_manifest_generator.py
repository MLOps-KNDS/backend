from schemas import pool_model as pool_model_schemas
from schemas import pool as pool_schemas
from .constants import Constants


class IstioVirtualServiceGenerator:
    def __init__(
        self,
        name: str,
        gateways_names: list[str],
        models: list[pool_model_schemas.PoolModel],
    ) -> None:
        """
        :param models: list of models to which the user will be redirected to
        :param pool_name: name of the pool
        """
        self.name = name
        self.gateways_names = gateways_names
        self.pool_models = models

    def generate(self) -> dict:
        """
        :return: Istio Virtual Service manifest
        """

        model_routes = [
            {
                "destination": {
                    "host": model.name,
                    "port": {"number": Constants.ISTIO_VIRTUAL_SERVICE_PORT},
                },
                "weight": model.weight,
            }
            for model in self.models
        ]

        body = {
            "apiVersion": "networking.istio.io/v1alpha3",
            "kind": "VirtualService",
            "metadata": {
                "name": self.name,
                "namespace": Constants.K8S_NAMESPACE_MODELS,
            },
            "spec": {
                "hosts": ["*"],
                "gateways": [gateway for gateway in self.gateways_names],
                "http": [{"route": model_routes}],
            },
        }
        return body


class IstioGatewayGenerator:
    def __init__(self, pools: list[pool_schemas.Pool], gateway_name: str) -> None:
        """
        :param gateway_name: name of the gateway
        :param pools: list of pools to which the user will be redirected to
        """
        self.name = gateway_name
        self.pools = pools

    def generate(self) -> dict:
        """
        :return: Istio Gateway manifest
        """

        gateway_servers = {
            "port": {
                "number": Constants.K8S_DEPLOYMENT_PORT,
                "name": "http",
                "protocol": "HTTP",
            },
            "hosts": [f"*/{pool.name}" for pool in self.pools],
        }

        body = {
            "apiVersion": "networking.istio.io/v1alpha3",
            "kind": "Gateway",
            "metadata": {
                "name": self.name,
                "namespace": Constants.K8S_NAMESPACE_MODELS,
            },
            "spec": {
                "selector": {"app": "ingressgateway"},
                "servers": gateway_servers,
            },
        }
        return body
