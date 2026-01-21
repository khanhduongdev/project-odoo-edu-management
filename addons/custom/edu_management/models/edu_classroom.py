from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EduClassroom(models.Model):
    _name = 'edu.classroom'
    _description = 'Phòng học'
    
    name = fields.Char('Tên phòng')
    capacity = fields.Integer('Sức chứa tối đa', default=20)
    location = fields.Char('Địa điểm')
    active = fields.Boolean(default=True)
    
    session_ids = fields.One2many('edu.session', 'classroom_id', string='Lớp học')

    @api.constrains('name', 'location')
    def _check_required_fields(self):
        for rec in self:
            if not rec.name or not rec.name.strip():
                raise ValidationError('Tên phòng không được bỏ trống!')
            if not rec.location or not rec.location.strip():
                raise ValidationError('Địa điểm không được bỏ trống!')

    @api.constrains('name', 'location')
    def _check_name_location(self):
        for rec in self:
            if rec.name and rec.location:
                name_clean = rec.name.strip()
                location_clean = rec.location.strip()
                domain = [
                    ('name', '=ilike', name_clean),
                    ('location', '=ilike', location_clean),
                    ('id', '!=', rec.id)
                ]
                if self.search_count(domain) > 0:
                    raise ValidationError('Tên phòng đã tồn tại tại địa điểm này!')

            if rec.capacity < 10:
                raise ValidationError('Sức chứa phải lớn hơn 10!')

    @api.depends('name', 'location')
    def _compute_display_name(self):
        for rec in self:
            if rec.location:
                rec.display_name = f"{rec.location} - {rec.name}"
            else:
                rec.display_name = rec.name
