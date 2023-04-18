import datetime
from typing import Dict

from src.schemas.model import Model
from src.schemas.test import Test


# Sample database for testing
model_db: Dict[int, Model] = {
    1: Model(
        id=1,
        name="model1",
        description="test description",
        created_at=datetime.datetime(2022, 7, 4, 21, 30, 57),
        created_by=1,
        updated_at=datetime.datetime(2022, 7, 6, 22, 50, 11),
        updated_by=12,
        image_tag="docker1",
        source_path="/source/path/1",
        status="active",
    ),
    2: Model(
        id=2,
        name="model2",
        description="test description",
        created_at=datetime.datetime.now(),
        created_by=13,
        updated_at=datetime.datetime(2022, 7, 6, 22, 50, 11),
        updated_by=12,
        image_tag="docker2",
        source_path="/source/path/2",
        status="active",
    ),
    3: Model(
        id=3,
        name="model3",
        description="test description3",
        created_at=datetime.datetime(2022, 7, 6, 22, 50, 12),
        created_by=1,
        updated_at=datetime.datetime.now(),
        updated_by=1,
        image_tag="docker3",
        source_path="/source/path/3",
    ),
    4: Model(
        id=4,
        name="model4",
        description="test description4",
        created_at=datetime.datetime.now(),
        created_by=1,
        updated_at=datetime.datetime.now(),
        updated_by=1,
        image_tag="docker4",
        source_path="/source/path/4",
    ),
    5: Model(
        id=5,
        name="model5",
        description="test description5",
        created_at=datetime.datetime.now(),
        created_by=1,
        updated_at=datetime.datetime.now(),
        updated_by=1,
        image_tag="docker5",
        source_path="/source/path/5",
    ),
    6: Model(
        id=6,
        name="model6",
        description="test description",
        created_at=datetime.datetime.now(),
        created_by=124,
        updated_at=datetime.datetime.now(),
        updated_by=1,
        image_tag="docker6",
        source_path="/source/path/6",
        status="active",
    ),
}

test_db: Dict[int, Test] = {
    1: Test(
        id=1,
        name="test",
        description="test_desc",
        created_at=datetime.datetime.now(),
        created_by=2,
        updated_at=datetime.datetime.now(),
        updated_by=1,
    )
}


def get_model_by_id(database: Dict[int, Model], model_id: int) -> Model | None:
    """
    Simple function to get model by id from the sample database
    :param database: database to get model from
    :param model_id: id of model to get
    :return: model if id was in database or None if wasn't
    """
    model = database.get(model_id)

    return model
