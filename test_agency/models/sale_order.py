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
    
    product_new_domain_ids = fields.Many2many(
        'product.template',
        'sale_order_line_product_domain_rel',
        'sale_order_line_id',
        'product_template_id',
        string='Productos Disponibles',
        compute='_compute_product_new_domain_ids',
        store=False,
        readonly=True
    )
    
    fecha_inicio = fields.Date(string="Fecha de inicio")
    fecha_fin = fields.Date(string="Fecha de fin")
    
    @api.depends('proveedor', 'tipo_servicio')
    def _compute_product_new_domain_ids(self):
        """Calcula los productos disponibles según proveedor y/o tipo de servicio"""
        for record in self:
            # Construir el dominio según la lógica requerida
            # Base: siempre incluir sale_ok
            domain = [('sale_ok', '=', True)]
            
            # Construir condiciones según qué campos tienen valor
            conditions = []
            
            if record.proveedor:
                conditions.append(('proveedor', '=', record.proveedor.id))
            
            if record.tipo_servicio:
                conditions.append(('tipo_servicio', '=', record.tipo_servicio.id))
            
            # Construir el dominio final
            if conditions:
                if len(conditions) == 1:
                    # Solo una condición: sale_ok AND condición
                    domain = ['&', ('sale_ok', '=', True)] + conditions
                else:
                    # Múltiples condiciones: sale_ok AND proveedor AND tipo_servicio
                    domain = ['&', ('sale_ok', '=', True), '&'] + conditions
            # Si no hay condiciones, domain ya tiene solo sale_ok
            
            # Buscar los productos y asignarlos al campo Many2many
            record.product_new_domain_ids = self.env['product.template'].search(domain)
    
    @api.onchange('proveedor', 'tipo_servicio')
    def _onchange_proveedor_tipo_servicio(self):
        """Filtra los productos disponibles según proveedor y/o tipo de servicio"""
        # Limpiar el producto cuando cambian los filtros
        if self.product_id:
            self.product_id = False
            self.name = False
        
        # Forzar el cálculo del campo computed
        self._compute_product_new_domain_ids()
        
        # Retornar el dominio para el campo product_template_id
        if self.product_new_domain_ids:
            return {
                'domain': {
                    'product_template_id': [('id', 'in', self.product_new_domain_ids.ids)]
                }
            }
        else:
            return {
                'domain': {
                    'product_template_id': [('sale_ok', '=', True)]
                }
            }
    
    @api.onchange('product_id')
    def _onchange_product_id_proveedor(self):
        """Valida y actualiza el proveedor cuando se selecciona un producto"""
        if self.product_id:
            product_proveedor = self.product_id.product_tmpl_id.proveedor
            if self.proveedor:

                if product_proveedor and product_proveedor != self.proveedor:

                    self.product_id = False
                    return {
                        'warning': {
                            'title': 'Proveedor no coincide',
                            'message': 'El producto seleccionado no pertenece al proveedor elegido. Por favor, seleccione un producto del proveedor correcto.'
                        }
                    }
            elif product_proveedor:

                self.proveedor = product_proveedor