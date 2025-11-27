# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    proveedor = fields.Char(
        string='Proveedor',
        help='Proveedor del producto'
    )
    
    tipo_servicio = fields.Many2one(
        'tipo.servicio',
        string='Tipo de Servicio',
        ondelete='set null',
        help='Tipo de servicio que representa el producto'
    )

