# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    proveedor = fields.Char(
        string='Proveedor',
        help='Proveedor del producto'
    )
    
    tipo_servicio = fields.Selection(
        [
            ('consultoria', 'Consultoría'),
            ('desarrollo', 'Desarrollo'),
            ('soporte', 'Soporte'),
            ('mantenimiento', 'Mantenimiento'),
            ('otro', 'Otro'),
        ],
        string='Tipo de Servicio',
        help='Tipo de servicio que representa el producto'
    )

