import datetime

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class OTRegistration(models.Model):
    _name = "ot.registration"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "employee_id"
    _description = "OT Registration"

    def _get_employee_id(self):
        employee_rec = self.env['hr.employee'].search([('user_id', '=', self.env.uid)],
                                                      limit=1)  # tìm kiếm user có trùng với employee đã tạo hay không
        return employee_rec.id

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, default=_get_employee_id,
                                  readonly=True)
    approve_id = fields.Many2one('hr.employee', string="Approver", store='True', required=True)
    department_lead_id = fields.Many2one('hr.employee', string='Department Lead',
                                         )
    project_manager_id = fields.Many2one('hr.employee', string='Project Manager')
    created_date = fields.Datetime('Created date', readonly=True, default=lambda self: fields.datetime.now())
    total_ot = fields.Float('OT Hours', compute='_compute_total_ot', readonly=True, store=True)
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'To Approve'),
                              ('pm_approved', 'PM Approved'), ('dl_approved', 'DL Approved'),
                              ('refused', 'Refused')],
                             default='draft', string='Status', tracking=True)
    ot_project_id = fields.One2many('ot.registration.line', 'ot_registration_id',
                                    string='OT Registration Project')
    project_id = fields.Many2one('ot.registration.project', string="Project", required=True)
    ot_month = fields.Char('OT Month', compute='_compute_ot_months', readonly=True, store=True)

    @api.depends("ot_project_id")
    def _compute_ot_months(self):
        for rec in self.ot_project_id:
            if rec.date_from and rec.date_to:
                self.ot_month = str(rec.date_from.month) + "/" + str(rec.date_to.year)

    @api.depends("ot_project_id")
    def _compute_total_ot(self):
        for rec in self.ot_project_id:
            if rec.date_from and rec.date_to:
                total = rec.date_to - rec.date_from
                self.total_ot = total.total_seconds() / 3600
                if self.total_ot > 48:
                    raise ValidationError("Thời gian đăng ký không được quá 2 ngày")

    def action_submit(self):

        self.state = 'to_approve'
        template = self.env.ref('ot_registration_module.ot_registration_email_request_pm_template')
        template.send_mail(self.id, force_send=True)

    def action_pm_approve(self):
        self.state = 'pm_approved'
        template = self.env.ref('ot_registration_module.ot_registration_email_request_dl_template')
        template.send_mail(self.id, force_send=True)

    def action_dl_approve(self):
        self.state = 'dl_approved'
        template = self.env.ref('ot_registration_module.ot_registration_email_dl_approved_template')
        template.send_mail(self.id, force_send=True)

    def action_pm_refuse(self):
        self.state = 'refused'
        template = self.env.ref('ot_registration_module.ot_registration_email_pm_refused_template')
        template.send_mail(self.id, force_send=True)

    def action_dl_refuse(self):
        self.state = 'refused'
        template = self.env.ref('ot_registration_module.ot_registration_email_dl_refused_template')
        template.send_mail(self.id, force_send=True)

    def action_draft(self):
        self.state = 'draft'
