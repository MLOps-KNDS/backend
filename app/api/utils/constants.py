import os


class Constants:
    # Google Cloud
    GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
    GCP_CREDENTIALS = os.environ.get("GCP_CREDENTIALS")
    GCP_CONTAINER_REGISTRY_URI = f"gcr.io/{GCP_PROJECT_ID}"

    # MLflow
    MLFLOW_ENV_MANAGER = os.environ.get("MLFLOW_ENV_MANAGER", "conda")

    # Kubernetes cluster
    K8S_NAMESPACE_MODELS = "models"
