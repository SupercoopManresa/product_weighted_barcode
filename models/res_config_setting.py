# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    weighted_product_barcode = fields.Boolean(
        related="company_id.weighted_product_barcode", string="Weighted Product Barode", readonly=False)

    barcode_rule_ids = fields.Many2one(
        'barcode.rule', related="company_id.barcode_rule_ids", string='Barcode Rule', readonly=False)
