# -*- coding: utf-8 -*-
from odoo import api, models
from random import choice
from string import digits
import re


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def write(self, vals):
        rule_id = self.env.user.company_id.barcode_rule_ids
        res = super(ProductTemplate, self).write(vals)
        if rule_id and 'to_weight' in vals and vals['to_weight'] == True or 'barcode' in vals:
            for variant in self.product_variant_ids:
                if variant.to_weight:
                    variant.barcode = variant.generate_barcode_for_weight(variant.barcode, rule_id)
        return res


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def generate_barcode_for_weight(self, barcode, rule_id):
        pattern = rule_id.pattern
        encoding = rule_id.encoding
        pattern_len = len(pattern) - 2
        numerical_content = re.search("[{][N]*[D]*[}]", pattern)
        if numerical_content:
            num_start = numerical_content.start()
            num_end = numerical_content.end()
            random_no = "".join(choice(digits) for i in range(pattern.count('.')))
            first_latter = re.findall('\d+', pattern)
            dynamic_no = (num_end - num_start - 2) * "0"
            new_barcode = first_latter[0] + random_no + dynamic_no + '_'
            if encoding == 'any':
                if not barcode or barcode and not barcode.startswith(first_latter[0]) or not len(barcode) == pattern_len or barcode[num_start:num_end] != dynamic_no:
                    new_barcode = new_barcode[0:-1]
            else:
                if not barcode or barcode and not rule_id.barcode_nomenclature_id.check_encoding(barcode, encoding):
                    if encoding == 'ean13':
                        last_digit = rule_id.barcode_nomenclature_id.ean_checksum(new_barcode)
                    if encoding == 'upca':
                        last_digit = rule_id.barcode_nomenclature_id.ean_checksum("0"+new_barcode)
                    if encoding == 'ean8':
                        last_digit = rule_id.barcode_nomenclature_id.ean8_checksum(new_barcode)
                    new_barcode = new_barcode.replace(new_barcode[-1], str(last_digit))
                else:
                    new_barcode = barcode
            return new_barcode

    @api.model_create_multi
    def create(self, vals_list):
        products = super(ProductProduct, self).create(vals_list)
        rule_id = self.env.user.company_id.barcode_rule_ids
        for res in products:
            if rule_id and res.to_weight:
                res.barcode = self.generate_barcode_for_weight(res.barcode, rule_id)
        return products

    def write(self, vals):
        rule_id = self.env.user.company_id.barcode_rule_ids
        if rule_id and 'to_weight' in vals and vals['to_weight'] == True or 'barcode' in vals:
            if self.to_weight:
                vals['barcode'] = self.generate_barcode_for_weight(self.barcode, rule_id)
        return super(ProductProduct, self).write(vals)
