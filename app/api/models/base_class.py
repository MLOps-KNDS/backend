from typing import Any
import re
from sqlalchemy.orm import as_declarative, declared_attr
from sqlalchemy import MetaData

metadata_obj = MetaData(schema="core")


@as_declarative(metadata=metadata_obj)
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        words = re.sub(r"([A-Z])", r" \1", cls.__name__).split()
        for i, word in enumerate(words):
            words[i] = word.lower()
        return "_".join(words)
