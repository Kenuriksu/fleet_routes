from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    batch_id = fields.Many2one(
        "batch.delivery",
        string="Batch Delivery"
    )