# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TipoServicio(models.Model):
    _name = 'tipo.servicio'
    _description = 'Tipo de Servicio'
    _order = 'name'

    name = fields.Char(
        string='Nombre',
        required=True,
        help='Nombre del tipo de servicio'
    )
    
    description = fields.Text(
        string='Descripción',
        help='Descripción del tipo de servicio'
    )
    
    active = fields.Boolean(
        string='Activo',
        default=True,
        help='Si está desactivado, este tipo de servicio no se mostrará en las listas'
    )

