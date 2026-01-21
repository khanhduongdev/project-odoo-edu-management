from odoo import models, fields

class EduSubject(models.Model):
    _name = 'edu.subject'
    _description = 'Môn học / Chuyên ngành'
    
    name = fields.Char('Tên môn học', required=True)
    code = fields.Char('Mã môn')
    description = fields.Text('Mô tả')
    active = fields.Boolean(default=True)
    
    course_ids = fields.One2many('edu.course', 'subject_id', string='Khóa học')
