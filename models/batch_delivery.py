from odoo import models, fields, api

class BatchDelivery(models.Model):
    _name = "batch.delivery"
    _description = "Batch Delivery"
    _order = "state asc, delivery_date desc"

    name = fields.Char(
        string="Batch ID",
        required=True,
        copy=False,
        readonly=True,
        default="New"
    )
    delivery_date = fields.Date()
    city = fields.Char()

    route_id = fields.Many2one("delivery.routes", string="Route Destination")
    truck_id = fields.Many2one("fleet.vehicle", string="Assigned Truck")

    order_ids = fields.Many2many("sale.order")

    driver_id = fields.Many2one("res.partner",string="Driver")
    helper_ids = fields.Many2many("res.partner", string="Helpers")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('assigned', 'Assigned'),
        ('done', 'Done')
    ], default='draft')

    def action_fetch_orders(self):
        for rec in self:
            orders = self.env['sale.order'].search([
                ('partner_shipping_id.city', '=', rec.city),
                ('commitment_date', '=', rec.delivery_date),
                ('state', '=', 'sale')
            ])

            rec.order_ids = [(6, 0, orders.ids)]

    @api.onchange('truck_id')
    def _onchange_truck_id(self):
        for rec in self:
            if rec.truck_id:
                rec.driver_id = rec.truck_id.driver_id
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('batch.delivery') or 'New'
        return super().create(vals_list)