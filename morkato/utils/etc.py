from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  Optional,
  Generator,
  Iterable,
  Callable,
  TypeVar,
  Literal,
  Union,
  List,
  overload
)

if TYPE_CHECKING:
  from morkato.context import MorkatoContext
  
  from discord.reaction import Reaction
  from discord.message import Message
  from discord.user import User

from numerize.numerize import numerize as num_fmt
from unidecode import unidecode

import re

FlagChecker = Literal['author', 'guild', 'channel', 'message']
T_co = TypeVar('T_co', covariant=True)
T = TypeVar('T')

def message_checker(ctx: MorkatoContext, flags: List[FlagChecker]):
  def check(message: Message) -> bool:
    if 'author' in flags and not message.author.id == ctx.author.id:
      return False
    
    if 'guild' in flags and not message.guild.id == ctx.guild.id:
      return False
    
    if 'channel' in flags and not message.channel.id == ctx.channel.id:
      return False
    
    return True
  
  return check

def reaction_checker(ctx: MorkatoContext, message: Message, flags: List[FlagChecker]):
  def check(reaction: Reaction, user: User) -> bool:
    if 'author' in flags and not user.id == ctx.author.id:
      return False
    
    if 'guild' in flags and reaction.message.guild and not reaction.message.guild.id == ctx.guild.id:
      return False
    
    if 'channel' in flags and not reaction.message.channel.id == ctx.channel.id:
      return False
    
    if 'message' in flags and not reaction.message.id == message.id:
      return False
    
    return True
  
  return check

class _EmptyMissingType:
  __slots__ = ()

  def __init__(self) -> None: ...
  def __repr__(self) -> str:
    return 'MISSING'

  def __bool__(self) -> bool:
    return False
  
  def __hash__(self) -> int:
    return 0

empty = _EmptyMissingType()

@overload
def in_range(num: int, range: tuple[float, float]) -> int: ...
@overload
def in_range(num: float, range: tuple[float, float]) -> float: ...
def in_range(num: Union[float, int], range: tuple[float, float]) -> Union[float, int]:
  min_n = min(range)
  max_n = max(range)

  return num >= min_n and num <= max_n

def find(iter: Iterable[T], check: Callable[[T], bool]) -> Generator[T, None, None]:
  return (item for item in iter if check(item))

def get(iter: Iterable[T], check: Callable[[T], bool]) -> Union[T, None]:
  return next(find(iter, check), None)

def is_empty_text(text: str) -> bool:
  return not text.strip()

def format_text(text: str, default: Optional[str] = None, /, **kwargs) -> str:
  default = default or ''

  def repl(match: re.Match) -> str:
    result = kwargs.get(match['key'], default)

    if not isinstance(result, str):
      return str(result)
    
    return result
  
  return re.sub(r'(?<!\\)\$(?P<key>[\w_]+)', repl, text, flags=re.IGNORECASE)

def strip_text(
  text: str, *,
  ignore_accents:   Optional[bool] = None,
  ignore_empty:     Optional[bool] = None,
  case_insensitive: Optional[bool] = None,
  strip_text:       Optional[bool] = None,
  empty: 						Optional[str]  = None
) -> str:
  if is_empty_text(text):
    return text
  
  empty = empty if empty is not None else '-'
  
  if strip_text:
    text = text.strip()

  if ignore_accents:
     text = unidecode(text)

  if ignore_empty:
     text = re.sub(r'\s+', empty, text)
  
  if case_insensitive:
     text = text.lower()

  return text

def fmt(text: str, *, empty: Optional[str] = None) -> str:
  return strip_text(
     text=text,
     ignore_accents=True,
     ignore_empty=True,
     case_insensitive=True,
     strip_text=True,
     empty=empty
  )