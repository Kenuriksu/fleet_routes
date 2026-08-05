from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    batch_id = fields.Many2one(
        "batch.delivery",
        string="Batch Delivery"
    )

    total_weight = fields.Float(
        string="Total Weight (kg)",
        compute="_compute_total_weight",
        store=True
    )

    @api.depends('order_line.product_id', 'order_line.product_uom_qty')
    def _compute_total_weight(self):
        for order in self:
            total = 0.0
            for line in order.order_line:
                if line.product_id:
                    total += (line.product_id.weight or 0.0) * line.product_uom_qty
            order.total_weight = total