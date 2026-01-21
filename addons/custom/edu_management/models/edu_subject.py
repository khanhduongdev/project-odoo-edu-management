from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EduSubject(models.Model):
    _name = 'edu.subject'
    _description = 'Môn học / Chuyên ngành'
    
    @api.model
    def _get_default_code(self):
        # Find all codes starting with SJ
        last_subject = self.search([('code', '=like', 'SJ%')], order='code desc', limit=1)
        if last_subject and last_subject.code:
            try:
                # Extract number part (SJ0020 -> 20)
                last_number = int(last_subject.code[2:])
                new_number = last_number + 1
            except ValueError:
                new_number = 1
        else:
            new_number = 1
            
        return f'SJ{new_number:04d}'

    name = fields.Char('Tên môn học')  # Remove required=True to customize error message
    code = fields.Char('Mã môn', readonly=True, copy=False, default=_get_default_code)
    description = fields.Text('Mô tả')
    active = fields.Boolean(default=True)
    
    course_ids = fields.One2many('edu.course', 'subject_id', string='Khóa học')

    @api.constrains('name')
    def _check_name(self):
        for rec in self:
            if not rec.name or not rec.name.strip():
                raise ValidationError('Tên môn học không được để trống')
                
            name_clean = rec.name.strip()
            domain = [
                ('name', '=ilike', name_clean),
                ('id', '!=', rec.id)
            ]
            if self.search_count(domain) > 0:
                raise ValidationError('Tên môn học đã tồn tại')
