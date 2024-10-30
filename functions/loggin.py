import dotenv
from os import environ
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from config import BotConfiguration as BotConfig
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from data.cookies import save_cookies, load_cookies
from utils import WebDriverTimeOuted as Wait

def loggin_shopify(driver: Edge):
  commit_botton = lambda: Wait(driver).until(EC.element_to_be_clickable((By.NAME, "commit")))
  
  input_email = Wait(driver).until(EC.visibility_of_element_located((By.ID, "account_email")))
  input_email.send_keys(environ["SHOPIFY_EMAIL"])
  commit_botton().click()
  input_password = Wait(driver).until(EC.visibility_of_element_located((By.ID, "account_password")))
  input_password.send_keys(environ["SHOPIFY_PASSWORD"])
  commit_botton().click()

  try:
    input_tfa_code = Wait(driver).until(EC.visibility_of_element_located((By.ID, "account_tfa_code")))
    # Admin Shopify
    dotenv.load_dotenv(override=True) # Restrictions to Loggin - Breackpoint debug python
    input_tfa_code.send_keys(environ["SHOPIFY_TFA_CODE"])
    commit_botton().click()
  except NoSuchElementException:
    print("No two factor verifier.")
    

def is_loggin_shopify(driver: Edge):
  return BotConfig.is_current_site(driver.current_url, "shopify_store_admin")

def is_loggin_stocky(driver: Edge):
  return BotConfig.is_current_site(driver.current_url, "stocky_loggin")


def loggin_stocky(driver: Edge):
  input_shop = Wait(driver).until(EC.visibility_of_element_located((By.ID, "shop")))
  input_shop.send_keys(BotConfig.sites["shopify_store"].hostname)
  submit_button = Wait(driver).until(EC.element_to_be_clickable((By.TAG_NAME, "button")))
  submit_button.click()


def loggin_web(driver: Edge):
  driver.get(BotConfig.sites["shopify_store_admin"].geturl())
  
  if not is_loggin_shopify(driver):
    url_loggin = BotConfig.sites["shopify_loggin"].geturl()
    driver.get(url_loggin)

    if not is_loggin_shopify(driver) and not load_cookies(driver):
      driver.get(url_loggin)
      is_page_loggin = BotConfig.is_current_site(driver.current_url, "shopify_loggin")
      if is_page_loggin:
        loggin_shopify(driver)
      save_cookies(driver)
  
  if not is_loggin_shopify(driver): return False
  driver.get(BotConfig.sites["stocky_loggin"].geturl())
  loggin_stocky(driver)
  save_cookies(driver)

  return is_loggin_stocky(driver)
  
