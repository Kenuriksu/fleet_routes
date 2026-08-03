from odoo import models, fields

class Routes(models.Model):
    _name = "delivery.routes"
    _description = "Delivery Routes"

    name = fields.Char(string="Route Name", required=True)
    destination = fields.Char(string="Destination")
    active = fields.Boolean(default=True)