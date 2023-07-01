from schemas import pool_model as pool_model_schemas
from .constants import Constants


class IstioVirtualServiceGenerator:
    def __init__(
        self,
        pool_name: str,
        gateways_names: list[str],
        models: list[pool_model_schemas.PoolModelDetailed],
    ) -> None:
        """
        :param models: list of models to which the user will be redirected to
        :param pool_name: name of the pool
        """
        self.pool_name = pool_name
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
            for model in self.pool_models
        ]

        body = {
            "apiVersion": "networking.istio.io/v1alpha3",
            "kind": "VirtualService",
            "metadata": {
                "name": self.pool_name,
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
    def __init__(self, gateway_name: str, pool_names: list[str]) -> None:
        """
        :param gateway_name: name of the gateway
        :param pools: list of pools to which the user will be redirected to
        """
        self.name = gateway_name
        self.pool_names = pool_names

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
            "hosts": [f"*/{pool_name}" for pool_name in self.pool_names],
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
                "servers": [gateway_servers],
            },
        }
        return body
