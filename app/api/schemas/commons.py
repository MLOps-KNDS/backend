from enum import Enum, EnumMeta


#  creates possibility to do for example:  if "owner" in Role
class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class BaseEnum(Enum, metaclass=MetaEnum):
    pass
