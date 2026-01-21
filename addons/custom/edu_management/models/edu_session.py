from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)

class EduSession(models.Model):
    _name = 'edu.session'
    _description = 'Lớp học'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc, name'
    
    # Basic fields
    name = fields.Char('Tên lớp', required=True, tracking=True)
    code = fields.Char('Mã lớp', readonly=True, copy=False)
    start_date = fields.Date('Ngày bắt đầu', required=True, tracking=True)
    duration = fields.Float('Thời lượng (ngày)', default=1.0)
    seats = fields.Integer('Số ghế', default=20)
    
    # Relations
    course_id = fields.Many2one('edu.course', string='Khóa học', 
        required=True, ondelete='restrict', tracking=True)
    instructor_id = fields.Many2one('res.partner', string='Giảng viên',
        domain=[('is_instructor', '=', True)], tracking=True)
    classroom_id = fields.Many2one('edu.classroom', string='Phòng học', tracking=True)
    attendee_ids = fields.Many2many('res.partner', 
        'edu_session_attendee_rel', 'session_id', 'partner_id',
        string='Học viên', domain=[('is_student', '=', True)])
    
    # Computed fields
    end_date = fields.Date('Ngày kết thúc', compute='_compute_end_date', 
        store=True)
    taken_seats = fields.Float('% Chỗ ngồi', compute='_compute_taken_seats')
    revenue = fields.Monetary('Doanh thu', compute='_compute_revenue', 
        currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', 
        default=lambda self: self.env.company.currency_id)
    
    # Workflow
    state = fields.Selection([
        ('draft', 'Dự thảo'),
        ('open', 'Mở đăng ký'),
        ('done', 'Kết thúc'),
        ('cancel', 'Hủy')
    ], default='draft', required=True, tracking=True)
    
    # Chức năng 13: Computed taken_seats
    @api.depends('seats', 'attendee_ids')
    def _compute_taken_seats(self):
        for rec in self:
            if rec.seats > 0:
                rec.taken_seats = (len(rec.attendee_ids) / rec.seats) * 100
            else:
                rec.taken_seats = 0
    
    # Chức năng 14: Computed end_date
    @api.depends('start_date', 'duration')
    def _compute_end_date(self):
        for rec in self:
            if rec.start_date and rec.duration:
                rec.end_date = rec.start_date + timedelta(days=rec.duration)
            else:
                rec.end_date = False
    
    # Chức năng 39: Computed revenue
    @api.depends('attendee_ids', 'course_id.fee_product_id')
    def _compute_revenue(self):
        for rec in self:
            if rec.course_id.fee_product_id:
                fee = rec.course_id.fee_product_id.list_price
                rec.revenue = len(rec.attendee_ids) * fee
            else:
                rec.revenue = 0
    
    # Chức năng 15: Onchange course_id
    @api.onchange('course_id')
    def _onchange_course_id(self):
        if self.course_id and self.course_id.responsible_id:
            # Auto-fill instructor from course responsible
            self.instructor_id = self.course_id.responsible_id
    
    # Chức năng 16: Onchange seats validation
    @api.onchange('seats')
    def _onchange_seats(self):
        if self.seats < 0:
            self.seats = 0
            return {
                'warning': {
                    'title': 'Cảnh báo',
                    'message': 'Số ghế không được âm! Đã reset về 0.'
                }
            }
    
    # Chức năng 17: Constraint - Giảng viên không được là học viên
    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_attendee(self):
        for rec in self:
            if rec.instructor_id and rec.instructor_id in rec.attendee_ids:
                raise ValidationError(
                    'Giảng viên không thể đồng thời là học viên của lớp này!'
                )
    
    # Chức năng bổ sung: Constraint - Capacity check
    @api.constrains('seats', 'classroom_id')
    def _check_capacity(self):
        for rec in self:
            if rec.classroom_id and rec.seats > rec.classroom_id.capacity:
                raise ValidationError(
                    f'Số ghế ({rec.seats}) không được vượt quá sức chứa của phòng '
                    f'{rec.classroom_id.name} ({rec.classroom_id.capacity} chỗ)!'
                )
    
    # Chức năng 18: Constraint - Duration validation
    @api.constrains('duration')
    def _check_duration(self):
        for rec in self:
            if rec.duration <= 0:
                raise ValidationError('Thời lượng khóa học phải lớn hơn 0!')
    
    # Chức năng bổ sung: Constraint - Instructor overlap
    @api.constrains('instructor_id', 'start_date', 'end_date')
    def _check_instructor_overlap(self):
        for rec in self:
            if rec.instructor_id and rec.start_date and rec.end_date:
                overlapping = self.search([
                    ('id', '!=', rec.id),
                    ('instructor_id', '=', rec.instructor_id.id),
                    ('state', 'not in', ['cancel']),
                    ('start_date', '<=', rec.end_date),
                    ('end_date', '>=', rec.start_date)
                ])
                if overlapping:
                    raise ValidationError(
                        f'Giảng viên {rec.instructor_id.name} đã có lịch dạy lớp '
                        f'{overlapping[0].name} trong khoảng thời gian này!'
                    )

    # Chức năng 28: Constraint - Classroom overlap
    @api.constrains('classroom_id', 'start_date', 'end_date')
    def _check_classroom_overlap(self):
        for rec in self:
            if rec.classroom_id and rec.start_date and rec.end_date:
                overlapping = self.search([
                    ('id', '!=', rec.id),
                    ('classroom_id', '=', rec.classroom_id.id),
                    ('state', 'not in', ['cancel']),
                    ('start_date', '<=', rec.end_date),
                    ('end_date', '>=', rec.start_date)
                ])
                if overlapping:
                    raise ValidationError(
                        f'Phòng {rec.classroom_id.name} đã có lớp '
                        f'{overlapping[0].name} trong khoảng thời gian này!'
                    )
    
    # Chức năng 20: Auto-generate code
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code'):
                vals['code'] = self.env['ir.sequence'].next_by_code('edu.session') or '/'
        return super().create(vals_list)
    
    # Chức năng 29: Custom name_get
    def name_get(self):
        result = []
        for rec in self:
            name = f'[{rec.code}] {rec.name}'
            if rec.start_date:
                name += f' - {rec.start_date.strftime("%d/%m/%Y")}'
            result.append((rec.id, name))
        return result
    
    # Chức năng 30: Default get
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        # Auto-fill start_date = tomorrow
        res['start_date'] = fields.Date.today() + timedelta(days=1)
        return res
    
    # Chức năng 40: Enhanced name_search
    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            args = ['|', '|', 
                    ('name', operator, name),
                    ('code', operator, name),
                    ('instructor_id.name', operator, name)] + args
        return super()._name_search(name, args, operator, limit, name_get_uid)
    
    # Chức năng 32: Action open
    def action_open(self):
        for rec in self:
            if not rec.classroom_id:
                raise UserError('Phải chọn phòng học trước khi mở đăng ký!')
            if not rec.instructor_id:
                raise UserError('Phải chọn giảng viên trước khi mở đăng ký!')
            rec.state = 'open'
    
    # Chức năng 33: Action done
    def action_done(self):
        self.write({'state': 'done'})
    
    # Chức năng 34: Action cancel
    def action_cancel(self):
        for rec in self:
            if rec.state == 'done':
                raise UserError('Không thể hủy lớp đã kết thúc!')
            rec.state = 'cancel'
    
    # Chức năng 37: Copy protection
    def copy(self, default=None):
        default = dict(default or {})
        default.update({
            'state': 'draft',
            'attendee_ids': [(5, 0, 0)],  # Clear all attendees
            'code': False,  # Generate new code
            'name': self.name + ' (Copy)',
        })
        return super().copy(default)
    
    # Chức năng 38: Unlink protection
    def unlink(self):
        for rec in self:
            if rec.state not in ['draft', 'cancel']:
                raise UserError(
                    'Chỉ có thể xóa lớp ở trạng thái Dự thảo hoặc Hủy!'
                )
        return super().unlink()
