# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    tag_ids = fields.Many2many(
        'product.tag',
        string="Tags")


class ProductTag(models.Model):
    _name = 'product.tag'

    name = fields.Char(translate=True, required=True)
    code = fields.Char(required=True)
