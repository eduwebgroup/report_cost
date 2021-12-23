from odoo import models, fields, api


class ManufactureOrder(models.Model):
    _inherit = 'mrp.production'

    currency_id = fields.Many2one('res.currency')
    unit_cost = fields.Float(string="Unit Cost", store=True, compute='_computeVar')
    total_cost = fields.Float(string="Total Cost", store=True, compute='_calculate_qty')

    @api.depends('move_raw_ids', 'move_raw_ids.cost')
    def _calculate_qty(self):
        for rec in self:
            cost_tot = 0
            for rs in rec.move_raw_ids:
                cost_tot = cost_tot + (rs.cost * rs.quantity_done)
            rec.total_cost = cost_tot

    @api.depends('total_cost', 'product_qty')
    def _computeVar(self):
        for record in self:
            record.unit_cost = record.total_cost/record.product_qty


class StockMove(models.Model):
    _inherit = 'stock.move'

    cost = fields.Float(related='product_id.standard_price', string="Cost", store=True, readonly=True)
