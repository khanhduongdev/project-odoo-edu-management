from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    # Default values as requested
    company_type = fields.Selection(default='person')
    
    # New Role Selection
    edu_role = fields.Selection([
        ('student', 'Học viên'),
        ('instructor', 'Giảng viên')
    ], string='Vai trò', default='student', required=True)
    
    # Computed booleans for backward compatibility and search
    is_instructor = fields.Boolean('Là giảng viên', compute='_compute_roles', store=True)
    is_student = fields.Boolean('Là học viên', compute='_compute_roles', store=True)
    
    session_teaching_ids = fields.One2many('edu.session', 'instructor_id', 
        string='Lớp đang dạy')
    session_attending_ids = fields.Many2many('edu.session', 
        'edu_session_attendee_rel', 'partner_id', 'session_id',
        string='Lớp đang học')
    
    # Smart button
    teaching_count = fields.Integer(compute='_compute_teaching_count')

    @api.depends('edu_role')
    def _compute_roles(self):
        for rec in self:
            rec.is_student = (rec.edu_role == 'student')
            rec.is_instructor = (rec.edu_role == 'instructor')

    @api.constrains('name', 'phone', 'email')
    def _check_required_fields(self):
        for rec in self:
            if not rec.name:
                raise ValidationError('Tên không được bỏ trống!')
            if not rec.phone:
                raise ValidationError('Số điện thoại không được bỏ trống!')
            if not rec.email:
                raise ValidationError('Email không được bỏ trống!')
    
    @api.constrains('email')
    def _check_email_validity(self):
        import re
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        for rec in self:
            if rec.email and not re.match(email_regex, rec.email):
                raise ValidationError('Email không hợp lệ (Định dạng: email@domain.com)!')

    @api.constrains('phone')
    def _check_phone_vietnam(self):
        import re
        phone_regex = r'^(0|\+84)(3|5|7|8|9)[0-9]{8}$'
        for rec in self:
            if rec.phone:
                phone_clean = rec.phone.replace(' ', '')
                if not re.match(phone_regex, phone_clean):
                    raise ValidationError('Số điện thoại không hợp lệ (Phải là số ĐT Việt Nam)!')
    
    @api.depends('session_teaching_ids')
    def _compute_teaching_count(self):
        for rec in self:
            rec.teaching_count = len(rec.session_teaching_ids)
    
    def action_view_teaching_sessions(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Lớp đang dạy',
            'res_model': 'edu.session',
            'domain': [('instructor_id', '=', self.id)],
            'view_mode': 'tree,form',
        }
