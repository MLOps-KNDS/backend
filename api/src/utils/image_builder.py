import logging
import docker
import mlflow

from src.utils.constants import Constants


_logger = logging.getLogger(__name__)


class ImageBuilder:
    """
    Builds a docker image from model's artifact.
    Allows to push it to Google Container Registry.

    Example:
    >>> image_builder = ImageBuilder(
    >>>    name="test2",
    >>>    model_uri="runs://f7b2b1e1d1e84b3e8b2b1e1d1e8bb3e8/model",
    >>> )
    >>> image_builder.build()
    >>> image_builder.push()
    """

    def __init__(self, name: str, model_uri: str) -> None:
        """
        :param name: name of the docker image
        :param model_uri: uri of the model's artifact
        """
        self.name: str = name
        self.model_uri: str = model_uri
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

    def push(self) -> str:
        """
        Pushes the docker image to Google Container Registry.

        :return: uri of the pushed image
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
        mlflow.models.build_docker(
            model_uri=self.model_uri,
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
