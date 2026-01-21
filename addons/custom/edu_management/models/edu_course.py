from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EduCourse(models.Model):
    _name = 'edu.course'
    _description = 'Khóa học'
    
    name = fields.Char('Tên khóa học', required=True)
    description = fields.Html('Mô tả')
    active = fields.Boolean(default=True)
    level = fields.Selection([
        ('basic', 'Cơ bản'),
        ('intermediate', 'Trung cấp'),
        ('advanced', 'Nâng cao')
    ], default='basic')
    
    responsible_id = fields.Many2one('res.partner', string='Người phụ trách', 
        domain=[('is_instructor', '=', True)])
    subject_id = fields.Many2one('edu.subject', string='Chuyên ngành')
    fee_product_id = fields.Many2one('product.template', 
        string='Học phí', domain=[('is_edu_fee', '=', True)])
    session_ids = fields.One2many('edu.session', 'course_id', string='Lớp học')
    
    session_count = fields.Integer(compute='_compute_session_count')
    
    @api.constrains('name')
    def _check_name_active(self):
        for rec in self:
            if rec.name:
                name_clean = rec.name.strip()
                domain = [
                    ('name', '=ilike', name_clean),
                    ('id', '!=', rec.id)
                ]
                if self.search_count(domain) > 0:
                    raise ValidationError('Tên khóa học đã tồn tại')
    
    @api.depends('session_ids')
    def _compute_session_count(self):
        for rec in self:
            rec.session_count = len(rec.session_ids)
            
            if rec.fee_product_id and rec.fee_product_id.detailed_type != 'service':
                raise ValidationError('Sản phẩm học phí phải là loại Dịch vụ (Service)!')
    
    @api.onchange('responsible_id')
    def _onchange_responsible_id(self):
        if self.responsible_id and self.responsible_id.email:
            email_info = f"Email: {self.responsible_id.email}"
            if self.description:
                self.description += email_info
            else:
                self.description = email_info
    
    def action_view_sessions(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Lớp học',
            'res_model': 'edu.session',
            'domain': [('course_id', '=', self.id)],
            'view_mode': 'tree,form',
        }
