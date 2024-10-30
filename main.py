import dotenv
from pathlib import Path
from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config import BotConfiguration
from functions.loggin import loggin_web
from functions.purchase_orders import create_purchase_order
from data.purchase_orders import PurchaseOrder
from utils import DIR_ROOT

def main():
  service = EdgeService(EdgeChromiumDriverManager().install())

  options = EdgeOptions()
  # options.add_argument("--headless")
  options.add_argument("--window-size=1024,800")
  options.add_argument(f"user-data-dir={DIR_ROOT.as_posix()}/data/nav_profile/")

  driver = Edge(options, service)

  # 1. Get access to Shopify and Stocky
  if loggin_web(driver):
    # 2. Test purchase order
    data_test_purchase_order = PurchaseOrder("./data/purchase_orders/compra_033333_20210214_0800.csv")
    create_purchase_order(driver, data_test_purchase_order)
    "add breakpoint - stop with debugger"
    
  driver.close()
  driver.quit()
  

if __name__ == "__main__":
  dotenv.load_dotenv()
  BotConfiguration.load_config()
  main()
