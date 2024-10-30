from typing import Literal, TypedDict
import json
from urllib.parse import urlparse, ParseResult as UrlParseResult

SitesURL = Literal[
  "shopify_store",
  "shopify_store_admin",
  "shopify_loggin",
  "stocky_loggin",
  "stocky_purchase_orders"
]

class ConfigWebDriver(TypedDict):
  wait_timeout: float

class Suppliers(TypedDict):
  index: int
  name: str
  nit: str

class PurchaseOrders(TypedDict):
  supplier_default: int
  timeout_add_products: int

class Locations(TypedDict):
  name_shopify: str
  name_d365: str
  code_store: str

class TaxType(TypedDict):
  name: str
  code: int
  rate: float

class BotConfiguration:
  def __new__(self):
    raise Exception("La clase 'BotConfiguration' no puede crear instancias.")
  
  web_driver: ConfigWebDriver = {}
  sites: dict[SitesURL, UrlParseResult] = {}
  purchase_orders: PurchaseOrders = {}
  locations: list[Locations]
  suppliers: list[Suppliers]
  sites_actions: dict[SitesURL, dict[str, str]] = {}
  tax_type: dict[str, TaxType] = {}

  @classmethod
  def load_config(cls, path_config=""):
    with open("./config.json", "r") as file_config:
      config: dict = json.load(file_config)

    for key, value in config.items():
      setattr(cls, key, value)

    cls.sites = { key: urlparse(url) for key, url in cls.sites.items() }


  @classmethod
  def is_current_site(cls, current_url: str, site: SitesURL):
    current_url: UrlParseResult = urlparse(current_url)
    return current_url.hostname == cls.sites[site].hostname


  @classmethod
  def get_current_site(cls, current_url: str):
    current_url: UrlParseResult = urlparse(current_url)
    
    for site, url in cls.sites.items():
      if url.hostname == current_url.hostname:
        return (site, url)
  
  @classmethod
  def get_site_action(cls, site: SitesURL, name_action: str, *var_format: str):
    try:
      url_action = cls.sites_actions[site][name_action]
    except KeyError:
      # logger
      raise KeyError("No se ha encontrado el nombre de la URL de la acción del sitio.")

    url = cls.sites[site].geturl()
    url = url[:-1] if url[-1] == "/" else url
    url_action = url_action if url_action[0] == "/" else "/" + url_action
    url_action = url_action.format(*var_format)
    return urlparse(url + url_action)
