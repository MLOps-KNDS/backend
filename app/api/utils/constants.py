import os
import base64


class Constants:
    # Google Cloud
    GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "test-gcp-project-id")
    GCP_CREDENTIALS_ENCODED = os.environ.get(
        "GCP_CREDENTIALS_ENCODED", "test-gcp-credentials-encoded"
    )
    GCP_CREDENTIALS = base64.b64decode(GCP_CREDENTIALS_ENCODED).decode("utf-8")

    GCP_CONTAINER_REGISTRY_URI = f"gcr.io/{GCP_PROJECT_ID}"

    # MLflow
    MLFLOW_ENV_MANAGER = os.environ.get("MLFLOW_ENV_MANAGER", "virtualenv")

    # Kubernetes cluster
    K8S_NAMESPACE_MODELS = "models"
    K8S_DEPLOYMENT_PORT = 8000
    K8S_SERVICE_PORT = 80
