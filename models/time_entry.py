from odoo import api, fields, models
from odoo.exceptions import ValidationError


class TimeEntry(models.Model):
    _name = 'time.entry'
    _description = 'Time Entry'
    _order = 'start_datetime desc, id desc'

    name = fields.Char(
        string='Description',
        required=True,
        default='New Time Entry',
    )
    user_id = fields.Many2one(
        'res.users',
        string='User',
        required=True,
        default=lambda self: self.env.user,
        index=True,
    )
    project_id = fields.Many2one(
        'project.project',
        string='Project',
        index=True,
    )
    task_id = fields.Many2one(
        'project.task',
        string='Task',
        domain="[('project_id', '=', project_id)]",
        index=True,
    )
    start_datetime = fields.Datetime(
        string='Start',
        readonly=True,
    )
    end_datetime = fields.Datetime(
        string='End',
        readonly=True,
    )
    duration = fields.Float(
        string='Duration (h)',
        compute='_compute_duration',
        store=True,
        digits=(16, 2),
    )
    duration_display = fields.Char(
        string='Duration',
        compute='_compute_duration',
        store=True,
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('running', 'Running'),
            ('done', 'Done'),
        ],
        string='Status',
        default='draft',
        required=True,
        index=True,
    )
    note = fields.Text(string='Notes')
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        required=True,
        default=lambda self: self.env['hr.employee'].search(
            [('user_id', '=', self.env.uid)], limit=1
        ),
        index=True,
    )
    timesheet_id = fields.Many2one(
        'account.analytic.line',
        string='Timesheet Entry',
        readonly=True,
        ondelete='set null',
    )
    partner_id = fields.Many2one(
        related='project_id.partner_id',
        string='Kunde',
        store=True,
        readonly=True,
    )

    # -------------------------------------------------------------------------
    # Compute
    # -------------------------------------------------------------------------

    @api.depends('start_datetime', 'end_datetime', 'state')
    def _compute_duration(self):
        now = fields.Datetime.now()
        for rec in self:
            start = rec.start_datetime
            if not start:
                rec.duration = 0.0
                rec.duration_display = '0h 0m'
                continue

            end = rec.end_datetime if rec.state == 'done' and rec.end_datetime else now
            delta = end - start
            total_seconds = max(delta.total_seconds(), 0)
            total_minutes = int(total_seconds // 60)
            hours = total_minutes // 60
            minutes = total_minutes % 60

            rec.duration = total_seconds / 3600.0
            rec.duration_display = f'{hours}h {minutes}m'

    # -------------------------------------------------------------------------
    # Constraints
    # -------------------------------------------------------------------------

    @api.constrains('state', 'user_id')
    def _check_one_running(self):
        for rec in self:
            if rec.state == 'running':
                running = self.search([
                    ('user_id', '=', rec.user_id.id),
                    ('state', '=', 'running'),
                    ('id', '!=', rec.id),
                ])
                if running:
                    raise ValidationError(
                        'Es läuft bereits ein Timer für diesen Benutzer. '
                        'Bitte stoppe den laufenden Timer zuerst.'
                    )

    # -------------------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------------------

    def action_start(self):
        self.ensure_one()
        running = self.search([
            ('user_id', '=', self.env.uid),
            ('state', '=', 'running'),
            ('id', '!=', self.id),
        ])
        if running:
            raise ValidationError(
                'Es läuft bereits ein Timer. '
                'Bitte stoppe den laufenden Timer zuerst.'
            )
        self.write({
            'state': 'running',
            'start_datetime': fields.Datetime.now(),
            'end_datetime': False,
        })

    def action_stop(self):
        self.ensure_one()
        now = fields.Datetime.now()
        self.write({'state': 'done', 'end_datetime': now})
        if self.project_id and self.employee_id:
            timesheet = self.env['account.analytic.line'].create({
                'name': self.name,
                'project_id': self.project_id.id,
                'task_id': self.task_id.id if self.task_id else False,
                'employee_id': self.employee_id.id,
                'unit_amount': self.duration,
                'date': now.date(),
            })
            self.timesheet_id = timesheet
