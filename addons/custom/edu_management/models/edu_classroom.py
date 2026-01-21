from odoo import models, fields

class EduClassroom(models.Model):
    _name = 'edu.classroom'
    _description = 'Phòng học'
    
    name = fields.Char('Tên phòng', required=True)
    capacity = fields.Integer('Sức chứa tối đa', default=20)
    location = fields.Char('Địa điểm')
    active = fields.Boolean(default=True)
    
    session_ids = fields.One2many('edu.session', 'classroom_id', string='Lớp học')
