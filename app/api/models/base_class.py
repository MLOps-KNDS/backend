from typing import Any
import re
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
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
