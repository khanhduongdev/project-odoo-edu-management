from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_edu_fee = fields.Boolean('Là học phí', default=False)
