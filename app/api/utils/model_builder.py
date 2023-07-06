import logging
import docker
import mlflow

from utils.constants import Constants

MODEL_IMAGE_NAME_PREFIX = "tyro-model-"


_logger = logging.getLogger(__name__)


class ModelBuilder:
    """
    Builds a docker image from model's artifact.
    Allows to push it to Google Container Registry.
    """

    def __init__(self, name: str, mlflow_tracking_uri: str, artifact_uri: str) -> None:
        """
        :param name: name of the docker image
        :param mlflow_tracking_uri: uri of the mlflow server
        :param artifact_uri: uri of the model's artifact
        """
        self.name: str = MODEL_IMAGE_NAME_PREFIX + name
        self.mlflow_tracking_uri: str = mlflow_tracking_uri
        self.artifact_uri: str = artifact_uri
        self.is_built: bool = False

    def build(self) -> None:
        """
        Builds a docker image from model's artifact.
        """
        try:
            _logger.info(f"Building a docker image with name {self.name}...")
            self.__build_mlflow_image()
            self.is_built = True
            _logger.info(f"Building a docker image with name {self.name} finished.")
        except Exception as e:
            _logger.error(
                f"Building a docker image with name {self.name} failed with error: {e}"
            )
            raise e

    @classmethod
    def build_base_image(cls) -> None:
        """
        Builds a base docker image with mlflow server.
        """
        try:
            _logger.info("Building a base mlflow docker image...")
            mlflow.models.build_docker(
                name=Constants.MLFLOW_BASE_IMAGE_NAME,
                env_manager=Constants.MLFLOW_ENV_MANAGER,
            )
            _logger.info("Building a base mlflow docker image finished.")
        except Exception as e:
            _logger.error(f"Building a base mlflow docker image failed with error: {e}")
            raise e

    def push(self) -> str:
        """
        Pushes the docker image to Google Container Registry.

        :return: tag of the pushed image
        """
        if not self.is_built:
            raise Exception("Image is not built yet.")
        try:
            _logger.info(f"Pushing a docker image with name {self.name}...")
            image_tag = self.__push_image_to_gcr()
            _logger.info(f"Pushing a docker image with name {self.name} finished.")
            return image_tag
        except Exception as e:
            _logger.error(
                f"Pushing a docker image with name {self.name} failed with error: {e}"
            )
            raise e

    def __build_mlflow_image(self) -> None:
        mlflow.set_tracking_uri(self.mlflow_tracking_uri)
        mlflow.models.build_docker(
            model_uri=self.artifact_uri,
            name=self.name,
            env_manager=Constants.MLFLOW_ENV_MANAGER,
        )

    def __push_image_to_gcr(self) -> str:
        client = docker.from_env()
        client.login(
            username="_json_key",
            password=Constants.GCP_CREDENTIALS,
            registry=Constants.GCP_CONTAINER_REGISTRY_URI,
        )
        image_tag = f"{Constants.GCP_CONTAINER_REGISTRY_URI}/{self.name}"
        client.images.get(self.name).tag(image_tag)

        for line in client.images.push(
            repository=image_tag,
            stream=True,
            decode=True,
        ):
            _logger.debug(line)

        return image_tag
