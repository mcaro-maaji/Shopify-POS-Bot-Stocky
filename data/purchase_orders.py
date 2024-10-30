from pathlib import Path
from data.data import AbstractData, DataRows

class DataPurchaseOrder(AbstractData):
  def __init__(self, path: Path | str):
    super().__init__(path)
    self.id: int | None = None
    self.number_purchase: int | None = None
    self.sku = DataRows(self, "sku")
    self.bar_code = DataRows(self, "bar_code")
    self.variant_shopify_id = DataRows(self, "variant_shopify_id")
    self.quantity = DataRows(self, "quantity")
    self.cost_price = DataRows(self, "cost_price")
    self.tax_type_id = DataRows(self, "tax_type_id")
    self.accounting_tax_type = DataRows(self, "accounting_tax_type")
    self.integration_code = DataRows(self, "integration_code")
    self.supplier_id = DataRows(self, "supplier_id")
    self.currency = DataRows(self, "currency")
    self.amount_paid = DataRows(self, "amount_paid")
    self.payment_due_on = DataRows(self, "payment_due_on")
    self.paid = DataRows(self, "paid")
    self.payment_on = DataRows(self, "payment_on")
    self.adjustments = DataRows(self, "adjustments")
    self.shipping = DataRows(self, "shipping")
    self.shipping_tax_type_id = DataRows(self, "shipping_tax_type_id")
    self.shopify_address_location_id = DataRows(self, "shopify_address_location_id")
    self.shopify_receive_location_id = DataRows(self, "shopify_receive_location_id")
    self.invoice_number = DataRows(self, "invoice_number")
    self.sequence_invoice_number = DataRows(self, "sequence_invoice_number")
    self.supplier_order_number = DataRows(self, "supplier_order_number")
    self.order_date = DataRows(self, "order_date")
    self.invoice_date = DataRows(self, "invoice_date")
    self.expected_on = DataRows(self, "expected_on")
    self.ship_on = DataRows(self, "ship_on")
    self.cancel_date = DataRows(self, "cancel_date")

