from .utils.primitives import IsString, IsNumber, IsEnum, IsList
from .validation import Base


class Serializer:
    Base = Base
    String = IsString
    Number = IsNumber
    Enum = IsEnum
    List = IsList


serializer = Serializer()
