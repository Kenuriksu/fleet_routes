from odoo import models, fields

class FleetTruck(models.Model):
    _inherit = "fleet.vehicle"

    helper_ids = fields.Many2many(
        "res.partner",
        string="Helpers"
    )