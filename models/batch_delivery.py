from odoo import models, fields, api
from odoo.fields import Datetime
from datetime import timedelta
from odoo.exceptions import ValidationError

class BatchDelivery(models.Model):
    _name = "batch.delivery"
    _inherit = ['mail.thread']
    _description = "Batch Delivery"
    _order = "state asc, delivery_date desc"
    _sql_constraints = [
        ('unique_batch_name', 'unique(name)', 'Batch ID must be unique!')
    ]

    name = fields.Char(
        string="Batch ID",
        required=True,
        copy=False,
        readonly=True,
        default="New"
    )
    delivery_date = fields.Date()

    route_id = fields.Many2one("delivery.routes", string="Route Destination", required=True)
    truck_id = fields.Many2one("fleet.vehicle", string="Assigned Truck")

    order_ids = fields.Many2many("sale.order", string="Delivery Orders")
    pick_line_ids = fields.One2many(
        "batch.delivery.pick.line",
        "batch_id",
        string="Pick List",
        compute="_compute_pick_lines",
        store=False
    )

    driver_id = fields.Many2one("res.partner",string="Driver")
    helper_ids = fields.Many2many("res.partner", string="Helpers")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('assigned', 'Assigned'),
        ('done', 'Done')
    ], default='draft')

    total_weight = fields.Float(
        string="Current Load (kg)",
        compute="_compute_total_weight",
        store=True
    )

    max_weight = fields.Float(
        related='truck_id.max_weight_kg',
        string="Truck Capacity (kg)",
        store=True
    )

    load_percentage = fields.Float(
        string="Load %",
        compute="_compute_load_percentage"
    )

    def action_fetch_orders(self):
        for rec in self:
            if not rec.delivery_date or not rec.route_id:
                continue

            start = Datetime.to_datetime(rec.delivery_date)
            end = start + timedelta(days=1)

            orders = self.env['sale.order'].search([
                ('partner_shipping_id.city', '=ilike', rec.route_id.name.strip()),
                ('commitment_date', '>=', start),
                ('commitment_date', '<', end),
                ('state', '=', 'sale'),
                ('fulfillment_type', '=', 'delivery'),
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
                seq = self.env['ir.sequence'].next_by_code('batch.delivery')
                vals['name'] = seq or 'B00000'
        return super().create(vals_list)

    @api.depends('order_ids.total_weight')
    def _compute_total_weight(self):
        for rec in self:
            rec.total_weight = sum(rec.order_ids.mapped('total_weight'))

    @api.depends('total_weight', 'max_weight')
    def _compute_load_percentage(self):
        for rec in self:
            if rec.max_weight:
                rec.load_percentage = (rec.total_weight / rec.max_weight) * 100
            else:
                rec.load_percentage = 0

    @api.constrains('order_ids', 'truck_id')
    def _check_weight_limit(self):
        for rec in self:
            if rec.max_weight and rec.total_weight > rec.max_weight:
                raise ValidationError(
                    f"Truck capacity exceeded!\n"
                    f"Max: {rec.max_weight} kg\n"
                    f"Current: {rec.total_weight} kg"
                )

    delivery_start = fields.Datetime(compute="_compute_dates", store=False)
    delivery_end = fields.Datetime(compute="_compute_dates", store=False)

    def _compute_dates(self):
        for rec in self:
            if rec.delivery_date:
                start = Datetime.to_datetime(rec.delivery_date)
                rec.delivery_start = start
                rec.delivery_end = start + timedelta(days=1)
            else:
                rec.delivery_start = False
                rec.delivery_end = False

    @api.depends('order_ids')
    def _compute_pick_lines(self):
        for rec in self:
            lines_map = {}

            for order in rec.order_ids:
                for line in order.order_line:
                    product = line.product_id

                    if product.id not in lines_map:
                        lines_map[product.id] = {
                            'product_id': product.id,
                            'quantity': 0,
                            'uom_id': line.product_uom.id,
                        }

                    lines_map[product.id]['quantity'] += line.product_uom_qty

            rec.pick_line_ids = [(0, 0, vals) for vals in lines_map.values()]

