from odoo import models, fields, api

class BatchDelivery(models.Model):
    _name = "batch.delivery"
    _description = "Batch Delivery"

    name = fields.Char(required=True, default="New Batch")

    delivery_date = fields.Date(required=True)
    city = fields.Char(required=True)

    route_id = fields.Many2one(
        "delivery.routes",
        string="Route"
    )

    model_id = fields.Many2one(
        "fleet.vehicle",
        string="Truck"
    )

    order_ids = fields.Many2many(
        "sale.order",
        string="Sales Orders"
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('assigned', 'Assigned'),
        ('done', 'Done')
    ], default='draft')