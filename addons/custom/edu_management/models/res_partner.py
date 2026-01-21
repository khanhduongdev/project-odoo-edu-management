from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    is_instructor = fields.Boolean('Là giảng viên', default=False)
    is_student = fields.Boolean('Là học viên', default=False)
    
    session_teaching_ids = fields.One2many('edu.session', 'instructor_id', 
        string='Lớp đang dạy')
    session_attending_ids = fields.Many2many('edu.session', 
        'edu_session_attendee_rel', 'partner_id', 'session_id',
        string='Lớp đang học')
    
    # Smart button
    teaching_count = fields.Integer(compute='_compute_teaching_count')
    
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
