import pickle
from config import BotConfiguration as BotConfig
from selenium.webdriver import Edge
from selenium.common.exceptions import InvalidCookieDomainException

def save_cookies(driver: Edge):
  current_site = BotConfig.get_current_site(driver.current_url)
  if current_site is None: return False
  [site, _] = current_site
  pickle.dump(driver.get_cookies(), open(f"./data/cookies/{site}.pkl", "wb"))
  return True


def load_cookies(driver: Edge):
  current_site = BotConfig.get_current_site(driver.current_url)
  if current_site is None: return False
  [site, url] = current_site

  try:
    cookies: list[dict] = pickle.load(open(f"./data/cookies/{site}.pkl", "rb"))
  except FileNotFoundError:
    # TODO: add to logger
    print(f"FileNotFoundError: No se encontró la cookie para el sitio '{site}'")
    return False
  
  for cookie in cookies:
    try:
      driver.add_cookie(cookie)
    except InvalidCookieDomainException:
      # TODO: add to logger
      print(f"InvalidCookieDomainException: No se puede añadir las cookie, se necesita hacer loggin en el sitio '{url.hostname}'")
    
  return True

