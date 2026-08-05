from odoo import models, fields

class Product(models.Model):
    _inherit = 'product.product'

    # Odoo already has weight, but ensure it's visible/used
    weight = fields.Float(string="Unit Weight (kg)")