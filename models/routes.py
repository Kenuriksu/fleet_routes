from odoo import models, fields

class Routes(models.Model):
    _name = "delivery.routes"
    _description = "Delivery Routes"

    name = fields.Char(string="City Destination", required=True)
    active = fields.Boolean(default=True)