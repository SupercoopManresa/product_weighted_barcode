# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    weighted_product_barcode = fields.Boolean(string="Weighted Product Barode")

    barcode_rule_ids = fields.Many2one(
        'barcode.rule', string='Barcode Rule')
