from urllib.parse import urlparse
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from config import BotConfiguration as BotConfig
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from data.purchase_orders import DataPurchaseOrder
from utils import WebDriverTimeOuted as Wait, CastToType

def new_purchase_order(driver: Edge):
  driver.get(BotConfig.get_site_action("stocky_purchase_orders", "create").geturl())
  dropdown = lambda id: Select(Wait(driver).until(EC.visibility_of_element_located((By.ID, id))))
  dropdown("vendor_or_supplier").select_by_visible_text("Supplier")

  # TODO: validate suppliers
  supplier_index = BotConfig.purchase_orders["supplier_default_index"]
  supplier = BotConfig.suppliers[supplier_index]
  dropdown("supplier_id").select_by_visible_text(supplier["name"])
  dropdown("generate").select_by_visible_text("Blank")

  # TODO: validate locations
  location = BotConfig.locations[1]["name_shopify"]
  dropdown("location_id").select_by_visible_text(location)

  Wait(driver).until(EC.element_to_be_clickable((By.NAME, "commit"))).click()


def set_id_data_purchase_order(driver: Edge, data: DataPurchaseOrder):
  Wait(driver).until(EC.url_matches(r"/\d+$"))
  url_purchase = urlparse(driver.current_url)
  
  # Obtener el id desde la URL ej. "https://stocky.shopifyapps.com/purchase_orders/[7135861]" <-- ID
  data.id = int(url_purchase.path.split("/")[-1])

  # Extraer el número de la orden desde el elemento visible en el DOM en la propiedad "value".
  # Al ser el elemento de tipo <input>, a nivel de interfaz se puede cambiar el número de la orden de compra (ADVERTENCIA de modificaciones).
  # El id del elemento <input> donde está el valor del numero de compra es la frase ("DataPurchaseOrder" + id de la compra)
  input_num_purchase = Wait(driver).until(EC.visibility_of_element_located((By.ID, f"DataPurchaseOrder{data.id}")))
  data.number_purchase = int(input_num_purchase.get_attribute("value"))


def add_products_purchase_order(driver: Edge, data: DataPurchaseOrder):
  driver.get(BotConfig.get_site_action("stocky_purchase_orders", "add_products", data.id).geturl())

  input_file = Wait(driver).until(EC.visibility_of_element_located((By.ID, "purchase_item_import_file_url")))
  input_file.send_keys(str(data._path.absolute()))
  timeout = BotConfig.purchase_orders["timeout_add_products"]
  input_summit = Wait(driver, timeout).until(EC.element_to_be_clickable((By.NAME, "commit")))
  input_summit.click()

  type_identifier_product = None
  if not data.bar_code.row is None:
    identifier_product = "bar_code"
    type_identifier_product = "Barcode"
  elif not data.sku.row is None:
    identifier_product = "sku"
    type_identifier_product = "SKU"
  elif not data.variant_shopify_id.row is None:
    identifier_product = "variant_shopify_id"
    type_identifier_product = "Shopify Variant ID"
  else: identifier_product = None

  if identifier_product is None:
    # Logger
    raise ValueError("Se requiere nombre de la columna que identifica al producto [bar_code, sku, variant_shopify_id]")
  
  dropdown = lambda id: Select(Wait(driver).until(EC.visibility_of_element_located((By.ID, id))))
  dropdown("indentifier_column").select_by_visible_text(identifier_product)
  dropdown("indentifier_type_column").select_by_visible_text(type_identifier_product)
  dropdown("quantity_column").select_by_visible_text("quantity")
  dropdown("cost_column").select_by_visible_text("cost_price")

  Wait(driver).until(EC.element_to_be_clickable((By.NAME, "commit"))).click()


def edit_shipping_purchase_order(driver: Edge, data: DataPurchaseOrder):
  current_url = driver.current_url
  shipping_is_none = data.shipping.row is None
  shipping_tax_type_is_none = data.shipping.row is None

  if not shipping_is_none or not shipping_tax_type_is_none:
    url_update_shipping = BotConfig.get_site_action("stocky_purchase_orders", "update_shipping", data.id).geturl()
    driver.get(url_update_shipping)
    if not shipping_is_none:
      driver.find_element(By.ID, f"purchase_order_shipping").send_keys = data.shipping.row
    
    shipping_tax_type = BotConfig.tax_type.get(data.shipping_tax_type_id.row)
    if not shipping_tax_type_is_none and not shipping_tax_type is None:
      select_tax_type = Select(driver.find_element(By.ID, f"purchase_order_shipping_tax_type"))
      select_tax_type.select_by_value=(data.shipping_tax_type_id.row)

    driver.find_element(By.ID, "commit").click()
    driver.get(current_url)

def _cast_to_date(date_str: str):
  return CastToType.date(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")

def fill_form_purchase_order(driver: Edge, data: DataPurchaseOrder):
  if data.id is None: return
  driver.get(BotConfig.get_site_action("stocky_purchase_orders", "select", data.id).geturl())

  def fill_element(id: str, send_keys: str, clear=True):
    element = driver.find_element(By.ID, id)
    if clear: element.clear()
    element.send_keys(str(send_keys))

  if not data.amount_paid.row is None:
    fill_element(f"total_field_{data.id}", data.amount_paid.row)

  if not data.paid.row is None:
    input_paid = driver.find_element(By.ID, "purchase_order_paid")
    is_paid = CastToType.bool(data.paid.row)
    is_input_paid_select = input_paid.is_selected()
    if (is_paid and not is_input_paid_select) or (not is_paid and is_input_paid_select):
      input_paid.click()

  if not data.adjustments.row is None:
    fill_element(f"purchase_order_adjustments", data.adjustments.row)

  if not data.invoice_number.row is None:
    fill_element(f"purchase_order_invoice_number", data.invoice_number.row)
  if not data.supplier_order_number.row is None:
    fill_element(f"purchase_order_supplier_order_number", data.supplier_order_number.row)

  payment_due_on = data.payment_due_on.rows_cast_to_type(1, _cast_to_date)
  payment_on = data.payment_on.rows_cast_to_type(1, _cast_to_date)
  order_date = data.order_date.rows_cast_to_type(1, _cast_to_date)
  invoice_date = data.invoice_date.rows_cast_to_type(1, _cast_to_date)
  ship_on = data.ship_on.rows_cast_to_type(1, _cast_to_date)
  expected_on = data.expected_on.rows_cast_to_type(1, _cast_to_date)
  cancel_date = data.cancel_date.rows_cast_to_type(1, _cast_to_date)
  if not payment_due_on is None:
    fill_element(f"purchase_order_payment_due_on", payment_due_on)
  if not payment_on is None:
    fill_element(f"purchase_order_paid_on", payment_on)
  if not order_date is None:
    fill_element(f"purchase_order_purchase_order_date", order_date)
  if not invoice_date is None:
    fill_element(f"purchase_order_invoice_date", invoice_date)
  if not ship_on is None:
    fill_element(f"purchase_order_ship_on", ship_on)
  if not expected_on is None:
    fill_element(f"purchase_order_expected_on", expected_on)
  if not cancel_date is None:
    fill_element(f"purchase_order_cancel_on", cancel_date)


def mark_ordered_purchase_order(driver: Edge, data: DataPurchaseOrder):
  if data.id is None: return
  url_purchase_to_mark = BotConfig.get_site_action("stocky_purchase_orders", "select", data.id).geturl()
  if driver.current_url != url_purchase_to_mark:
    driver.get(url_purchase_to_mark)
  path_url = BotConfig.get_site_action("stocky_purchase_orders", "mark_ordered", data.id).path
  anchor_mark_ordered = Wait(driver).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"a[href=\"{path_url}\"]")))
  anchor_mark_ordered.click()


def create_purchase_order(driver: Edge, data: DataPurchaseOrder):
  new_purchase_order(driver)
  set_id_data_purchase_order(driver, data)
  add_products_purchase_order(driver, data)
  fill_form_purchase_order(driver, data)
  mark_ordered_purchase_order(driver, data)
  "add brackpoint - stop with debugger"

