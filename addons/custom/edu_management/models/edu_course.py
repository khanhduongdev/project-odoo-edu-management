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
    
    # Relations
    responsible_id = fields.Many2one('res.users', string='Người phụ trách')
    subject_id = fields.Many2one('edu.subject', string='Chuyên ngành')
    fee_product_id = fields.Many2one('product.template', 
        string='Học phí', domain=[('is_edu_fee', '=', True)])
    session_ids = fields.One2many('edu.session', 'course_id', string='Lớp học')
    
    # Smart button
    session_count = fields.Integer(compute='_compute_session_count')
    
    # _sql_constraints = [
    #     ('name_unique', 'UNIQUE(name)', 'Tên khóa học phải duy nhất!')
    # ]

    @api.constrains('name')
    def _check_name_active(self):
        for rec in self:
            if rec.name:
                # Check duplication (Case insensitive + Strip whitespace)
                name_clean = rec.name.strip()
                domain = [
                    ('name', '=ilike', name_clean),
                    ('id', '!=', rec.id)
                ]
                if self.search_count(domain) > 0:
                    raise ValidationError(f'Tên khóa học "{name_clean}" đã tồn tại (không phân biệt hoa thường)!')
    
    @api.depends('session_ids')
    def _compute_session_count(self):
        for rec in self:
            rec.session_count = len(rec.session_ids)
            
    @api.constrains('fee_product_id')
    def _check_fee_product(self):
        for rec in self:
            if rec.fee_product_id and rec.fee_product_id.detailed_type != 'service':
                raise ValidationError('Sản phẩm học phí phải là loại Dịch vụ (Service)!')
    
    def action_view_sessions(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Lớp học',
            'res_model': 'edu.session',
            'domain': [('course_id', '=', self.id)],
            'view_mode': 'tree,form',
        }
