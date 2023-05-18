from schemas import model as model_schemas
from .constants import Constants


class IstioManifestGen:
    def generate_vs_manifest(models: list[model_schemas.Model], pool_name: str) -> dict:
        body = {
            "apiVersion": f"{Constants.GROUP}/{Constants.VERSION}",
            "kind": "VirtualService",
            "metadata": {"name": pool_name},
            "spec": {
                "hosts": ["*"],
                "http": [
                    {
                        "route": [
                            {
                                "destination": {
                                    "host": f"{model.name}",
                                    "port": {"number": 80},
                                }
                            }
                            for model in models
                        ]
                    }
                ],
            },
        }
        return body
