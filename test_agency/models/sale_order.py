from odoo import fields, models, api
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
        help='Seleccione un proveedor para filtrar los productos disponibles'
    )
    tipo_servicio = fields.Many2one(
        'tipo.servicio',
        string='Tipo de servicio',
        # related='product_id.product_tmpl_id.tipo_servicio',
        store=True,
    )
    
    fecha_inicio = fields.Date(string="Fecha de inicio")
    fecha_fin = fields.Date(string="Fecha de fin")
    
    @api.onchange('proveedor')
    def _onchange_proveedor(self):
        """Filtra los productos disponibles según el proveedor seleccionado"""
        # Siempre limpiar el producto cuando cambia el proveedor para forzar la selección correcta
        if self.product_id:
            self.product_id = False
            self.name = False
        
        if self.proveedor:
            # Filtrar productos para mostrar solo los del proveedor seleccionado
            # Combinar con el dominio de sale_ok que ya existe
            return {
                'domain': {
                    'product_id': ['&', ('sale_ok', '=', True), ('product_tmpl_id.proveedor', '=', self.proveedor.id)],
                    'product_template_id': ['&', ('sale_ok', '=', True), ('proveedor', '=', self.proveedor.id)]
                }
            }
        else:
            # Si no hay proveedor, mostrar todos los productos con sale_ok
            return {
                'domain': {
                    'product_id': [('sale_ok', '=', True)],
                    'product_template_id': [('sale_ok', '=', True)]
                }
            }
    
    @api.onchange('product_id')
    def _onchange_product_id_proveedor(self):
        """Valida y actualiza el proveedor cuando se selecciona un producto"""
        if self.product_id:
            product_proveedor = self.product_id.product_tmpl_id.proveedor
            if self.proveedor:
                # Si hay un proveedor seleccionado, validar que coincida
                if product_proveedor and product_proveedor != self.proveedor:
                    # Si no coincide, limpiar el producto y mostrar advertencia
                    self.product_id = False
                    return {
                        'warning': {
                            'title': 'Proveedor no coincide',
                            'message': 'El producto seleccionado no pertenece al proveedor elegido. Por favor, seleccione un producto del proveedor correcto.'
                        }
                    }
            elif product_proveedor:
                # Si no hay proveedor seleccionado, actualizarlo automáticamente
                self.proveedor = product_proveedor