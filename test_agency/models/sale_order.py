from odoo import fields, models
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    pax = fields.Char()
    adt = fields.Integer(string='numero de pasajeros adultos')
    chd = fields.Integer(string='numero de niños')
    age = fields.Integer(string='edad de niños')
    check_in = fields.Date(string='fecha de ingreso')
    check_out = fields.Date(string='fecha de salida')
    room_type = fields.Selection([
    ('swb', 'Habitación simple'),
    ('dwb', 'Habitación doble'),
    ('trp', 'Habitación triple'),], string="Tipo de habitación")
    agency_id = fields.Many2one(
        'res.partner',
        string='Agencia',
        related='partner_id.commercial_partner_id',
        store=True, readonly=True)
    counter_id = fields.Many2one(
        'res.partner',
        string='Counter (vendedor)',
        domain="[('parent_id', '=', agency_id)]")
    

class SaleOrderLine(models.Model):
    _inherit= 'sale.order.line'
    
    proveedor = fields.Many2one(
        'res.partner',
        string='Proveedor',
        related='product_id.product_tmpl_id.proveedor',
        store=True, readonly=True,
    )
    tipo_servicio = fields.Many2one(
        'tipo.servicio',
        string='Tipo de servicio',
        related='product_id.product_tmpl_id.tipo_servicio',
        store=True, readonly=True,
    )
    
    fecha_inicio = fields.Date(string="Fecha de inicio")
    fecha_fin = fields.Date(string="Fecha de fin")
    
    
    