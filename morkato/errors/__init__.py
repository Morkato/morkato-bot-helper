from __future__ import annotations

from typing_extensions import Self
from typing import (
  TYPE_CHECKING,
  Optional,
  ClassVar,
  Tuple,
  Type,
  Dict,
  Any
)

from enum import Enum

class ErrorType(Enum):
  GENERIC: ClassVar[str] = "generic.unknown"
  GENERIC_NOTFOUND: ClassVar[str] = "generic.unknown"

  ENDPOINT_NOTFOUND: ClassVar[str] = "endpoint.notfound"
  GUILD_NOTFOUND: ClassVar[str] = "guild.notfound"

  def __repr__(self) -> str:
    return repr(self.value)
  
  def __str__(self) -> str:
    return str(self.value)
  
  def __hash__(self) -> int:
    return hash(self.value)

  def __eq__(self, other: Any) -> bool:
    return self.value == other

def geterr(type: Optional[ErrorType] = None, *, message: Optional[str] = None, messages: Optional[Dict[str, str]] = None) -> BaseError:
  cls: Type[BaseError] = BaseError

  if not type:
    return cls(message, messages=messages)
  
  if type in (
    ErrorType.GUILD_NOTFOUND
  ):
    cls = Notfound
  
  return cls(message, messages=messages)

class BaseErrorMeta(type):
  DEFAULT_MESSAGE: ClassVar[str] = "Erro interno, desculpe-me."
  DEFAULT_TYPE: ClassVar[ErrorType] = ErrorType.GENERIC
  DEFAULT_MESSAGES: ClassVar[Dict[str, str]] = {
    ErrorType.GUILD_NOTFOUND: "Esse servidor requer configuração."
  }
  
  def __new__(cls, name: str, bases: Tuple[Type[Any]], attrs: Dict[str, Any], /, **kwargs) -> Self:
    message = kwargs.pop('message', "Erro interno, desculpe-me.")
    type = kwargs.pop('type', ErrorType.GENERIC)

    if not isinstance(type, ErrorType):
      type = ErrorType.GENERIC

    for (key, value) in attrs.items():
      if key == 'DEFAULT_MESSAGES':
        if not isinstance(value, dict):
          value = dict()
        
        value.update(BaseErrorMeta.DEFAULT_MESSAGES)
        attrs[key] = value
        
        break
    
    message = message if isinstance(message, str) else str(message)

    attrs['DEFAULT_MESSAGE'] = message
    attrs['DEFAULT_TYPE'] = type

    return super().__new__(cls, name, bases, attrs, **kwargs)

class BaseError(Exception, metaclass=BaseErrorMeta):
  def __init__(
    self,
    message:  Optional[str]            = None,
    type:     Optional[ErrorType]      = None, *,
    messages: Optional[Dict[str, str]] = None
  ) -> None:
    super().__init__()

    cls = self.__class__

    type = type or cls.DEFAULT_TYPE

    if messages is None:
      messages = {  }
    
    messages.update(cls.DEFAULT_MESSAGES)
    
    self.message = message or messages.get(type, cls.DEFAULT_MESSAGE)
    self.type = type
  
  def get_logging_error(self) -> str:
    return '[%s: %s] %s' % (
      self.__class__.__name__,
      self.type,
      self.message
    )
  
  def get_discord_message(self) -> str:
    return "**`%s`**" % self.get_logging_error()

class MessageErrorDiscordLogging(BaseError):
  def get_discord_message(self) -> str:
    return self.message

class EndpointNotfound(MessageErrorDiscordLogging, message="Ocorreu algum erro, esse endpoint não existe.", type=ErrorType.ENDPOINT_NOTFOUND): ...
class Notfound(MessageErrorDiscordLogging, message="Item não encontrado.", type=ErrorType.GENERIC_NOTFOUND): ...