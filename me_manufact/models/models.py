from odoo import models, fields, api, SUPERUSER_ID, _


class ManufactureInherit(models.Model):
    _inherit = "mrp.production"

    currency_id = fields.Many2one("res.currency", string="Currency")
    unit_cost = fields.Monetary(string="Unit Cost")
    total_cost = fields.Monetary(string="Total Cost", compute='_computeVar')

    @api.depends('unit_cost', 'product_qty')
    def _computeVar(self):
        for record in self:
            record.total_cost = record.unit_cost * record.product_qty
