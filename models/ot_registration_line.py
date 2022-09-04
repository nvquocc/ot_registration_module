from odoo import fields, models, api, _
from datetime import date, datetime
from odoo.exceptions import ValidationError


class OTRegistrationLine(models.Model):
    _name = "ot.registration.line"
    date_from = fields.Datetime(string="From", required=True)
    date_to = fields.Datetime(string="To", required=True)
    ot_hours = fields.Float(string="OT Hours", compute='_compute_ot_hours', readonly=True)
    ot_category = fields.Selection(selection=[('normal_day', 'Ngày bình thường'),
                                              ('normal_day_morning', 'OT ban ngày (6h - 8h30)'),
                                              ('normal_day_night', 'Ngày bình thường - Ban đêm'),
                                              ('saturday', 'Thứ 7'),
                                              ('sunday', 'Chủ nhật'),
                                              ('weekend_day_night', 'Ngày cuối tuần - Ban đêm'),
                                              ('holiday', 'Ngày lễ'),
                                              ('holiday_day_night', 'Ngày lễ - Ban đêm'),
                                              ('compensatory_normal', 'Bù ngày lễ vào ngày thường'),
                                              ('compensatory_night', 'Bù ngày lễ vào ban đêm')], default='normal_day',
                                   required=True,
                                   string='OT Category')
    wfh = fields.Boolean(string="WFH")
    job_taken = fields.Char(string="Job Taken")
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'To Approve'),
                              ('pm_approved', 'PM Approved'), ('dl_approved', 'DL Approved'),
                              ('refused', 'Refused')],
                             default='draft', string='State')
    late_approved = fields.Boolean('Late Approved')
    hr_note = fields.Char(string="HR Notes")
    attendance_note = fields.Char(string="Attendance Notes")
    warning_note = fields.Char(string='Warning')
    ot_registration_id = fields.Many2one('ot.registration', string="OT Registration ID")


    @api.depends("date_from", "date_to")
    def _compute_ot_hours(self):
        for record in self:
            if record.date_from and record.date_to:
                total = record.date_to - record.date_from
                record.ot_hours = total.total_seconds() / 3600

    @api.constrains("ot_hours")
    def _check_ot_hours(self):
        if self.ot_hours <= 0:
            raise ValidationError("Số giờ OT phải lớn hơn 0")

    def action_submit(self):
        self.state = 'to_approve'

    def action_pm_approve(self):
        self.state = 'pm_approved'

    def action_dl_approve(self):
        self.state = 'dl_approved'

    def action_refuse(self):
        self.state = 'refused'

    def action_draft(self):
        self.state = 'draft'
