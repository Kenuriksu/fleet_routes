from odoo import models, fields

class FleetTruck(models.Model):
    _inherit = "fleet.vehicle"

    helper_ids = fields.Many2many(
        "res.partner",
        string="Helpers"
    )

    max_weight_kg = fields.Float(
        string="Max Load (kg)",
        help="Maximum carrying capacity of the truck in kilograms"
    )