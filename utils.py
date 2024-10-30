from typing import Iterable
from time import strptime
from datetime import date
from pathlib import Path
from selenium.types import WaitExcTypes
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import POLL_FREQUENCY
from selenium.webdriver.remote.webdriver import WebDriver
from config import BotConfiguration as BotConfig

class CastToType:
  @staticmethod
  def int(value: str):
    return int(value)
  
  @staticmethod
  def float(value: str):
    return float(value)
    
  @staticmethod 
  def bool(
    value: str,
    match_true: list[str] = ["true", "True"]
  ):
    if value in match_true: return True
    return False
  
  @staticmethod
  def date(value: str, format="%a %b %d %H:%M:%S %Y"):
    return date(*strptime(value, format)[:3])


def range_slice_to_int(slice: slice) -> int:
  start = slice.start or 0
  stop = slice.stop or 0
  return start + stop

DIR_ROOT = Path(".").absolute()


class WebDriverTimeOuted(WebDriverWait):
  def __init__(self, driver: WebDriver, timeout: float | None = None, poll_frequency: float = POLL_FREQUENCY, ignored_exceptions: WaitExcTypes | None = None):
    if timeout is None: timeout = BotConfig.web_driver["wait_timeout"]
    super().__init__(driver, timeout, poll_frequency, ignored_exceptions)

