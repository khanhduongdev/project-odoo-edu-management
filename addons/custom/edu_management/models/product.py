from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_edu_fee = fields.Boolean('Là học phí', default=False)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        # Check context specific for Tuition Fee menu action
        if self.env.context.get('default_is_edu_fee'):
            # Find last code starting with EF
            last_fee = self.search([
                ('is_edu_fee', '=', True), 
                ('default_code', '=like', 'EF%')
            ], order='default_code desc', limit=1)
            
            if last_fee and last_fee.default_code:
                try:
                    # EF0001 -> 1
                    last_number = int(last_fee.default_code[2:])
                    new_number = last_number + 1
                except ValueError:
                    new_number = 1
            else:
                new_number = 1
            
            res['default_code'] = f'EF{new_number:04d}'
        return res

    @api.constrains('list_price')
    def _check_fee_price(self):
        for rec in self:
            if rec.is_edu_fee and rec.list_price < 0:
                raise ValidationError('Học phí không được âm!')
