from odoo import fields, models

class CrmTeamSalesman(models.Model):
    _inherit = 'res.users'
    
    is_counter = fields.Boolean('Es Vendedor')
    
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    counter_id = fields.Many2one(
        comodel_name='res.users',
        domain=[ ('is_counter', '=', True), ('active', 'in', [True, False])]
        )
    