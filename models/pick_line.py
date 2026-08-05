from odoo import models, fields, api

class BatchDeliveryPickLine(models.Model):
    _name = "batch.delivery.pick.line"
    _description = "Batch Delivery Pick Line"

    batch_id = fields.Many2one("batch.delivery", ondelete="cascade")

    product_id = fields.Many2one("product.product", required=True)
    quantity = fields.Float(string="Total Quantity")
    uom_id = fields.Many2one("uom.uom", string="UoM")