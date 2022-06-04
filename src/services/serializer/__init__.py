from .utils.primitives import IsString, IsNumber, IsEnum, IsList, ExistsRule, EmailRule
from .validation import Base


class Serializer:
    Base = Base
    String = IsString
    Number = IsNumber
    Enum = IsEnum
    List = IsList
    Exists = ExistsRule
    Email = EmailRule


serializer = Serializer()
