from schemas import pool_model as pool_model_schemas
from schemas import pool as pool_schemas
from .constants import Constants


class IstioVirtualServiceGenerator:
    def __init__(
        self,
        models: list[pool_model_schemas.PoolModel],
        pool_name: str,
        gatewaway_name: str,
    ) -> None:
        """
        :param models: list of models to which the user will be redirected to
        :param pool_name: name of the pool
        """
        self.pool_models = models
        self.gateaway_name = gatewaway_name
        self.name = pool_name

    def generate(self) -> dict:
        """
        :return: Istio Virtual Service manifest
        """

        model_routes = [
            {
                "destination": {
                    "host": model.name,
                    "port": {"number": Constants.K8S_SERVICE_PORT},
                },
                "weight": model.weight,
            }
            for model in self.models
        ]

        body = {
            "apiVersion": "networking.istio.io/v1alpha3",
            "kind": "VirtualService",
            "metadata": {"name": self.name, "namespace": f"pool-config-{self.name}"},
            "spec": {
                "hosts": ["*"],
                "gateways": [
                    f"gateaway-config-{self.gateaway_name}/{self.gateaway_name}"
                ],
                "http": [{"route": model_routes}],
            },
        }
        return body


class IstioGatewayGenerator:
    def __init__(self, pools: list[pool_schemas.Pool], gateaway_name: str) -> None:
        """
        :param gateaway_name: name of the gateaway
        :param pools: list of pools to which the user will be redirected to
        """
        self.name = gateaway_name
        self.pools = pools

    def generate(self) -> dict:
        """
        :return: Istio Gateaway manifest
        """

        gateaway_servers = {
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
                "namespace": f"gateaway-config-{self.name}",
            },
            "spec": {
                "selector": {"app": "ingressgateway"},
                "servers": gateaway_servers,
            },
        }
        return body
