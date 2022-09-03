from odoo import models, api, fields
import datetime


class OTRegistrationProject(models.Model):
    _name = "ot.registration.project"
    _rec_name = "name_project"
    name_project = fields.Char(string="Tên dự án", required=True)
    department_id = fields.Many2one('hr.department', string='Tên phòng ban', required=True)
    employee_id = fields.Many2one('hr.employee', string="Tên nhân viên", required=True)
    created_date = fields.Datetime(string="Created Date", default=lambda self: fields.datetime.now())
    status = fields.Selection(string='Trạng thái',
                              selection=[('open', 'Open'), ('closing', 'Closing'), ('close', 'Closed')], default='open')
    note = fields.Text(string="Ghi chú")
    company = fields.Text(string="Tên công ty")

