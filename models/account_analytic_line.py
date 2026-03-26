# -*- coding: utf-8 -*-
import datetime

from odoo import api, fields, models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    time_entry_id = fields.Many2one(
        'time.entry',
        string='Time Tracker Eintrag',
        readonly=True,
        ondelete='set null',
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if not self.env.context.get('from_time_tracker'):
            for rec in records:
                if rec.project_id:
                    rec._sync_to_time_entry()
        return records

    def write(self, vals):
        res = super().write(vals)
        if not self.env.context.get('from_time_tracker'):
            if any(f in vals for f in ('unit_amount', 'date', 'name', 'task_id')):
                for rec in self:
                    if rec.project_id:
                        rec._sync_to_time_entry()
        return res

    def _sync_to_time_entry(self):
        if not self.project_id or not self.employee_id or not self.unit_amount:
            return

        entry_date = self.date

        # Startzeit: nach dem letzten Eintrag des Tages, Fallback 08:00
        day_start = datetime.datetime.combine(entry_date, datetime.time.min)
        day_end = datetime.datetime.combine(entry_date, datetime.time.max)
        exclude_id = self.time_entry_id.id if self.time_entry_id else 0
        last_entry = self.env['time.entry'].search([
            ('employee_id', '=', self.employee_id.id),
            ('state', '=', 'done'),
            ('end_datetime', '>=', day_start),
            ('end_datetime', '<=', day_end),
            ('id', '!=', exclude_id),
        ], order='end_datetime desc', limit=1)

        start_dt = last_entry.end_datetime if last_entry else \
            datetime.datetime.combine(entry_date, datetime.time(8, 0))
        end_dt = start_dt + datetime.timedelta(hours=self.unit_amount)
        user = self.employee_id.user_id or self.env.user

        if self.time_entry_id:
            self.time_entry_id.with_context(from_analytic_line=True).write({
                'name': self.name or 'Timesheet Eintrag',
                'start_datetime': start_dt,
                'end_datetime': end_dt,
                'project_id': self.project_id.id,
                'task_id': self.task_id.id if self.task_id else False,
            })
        else:
            time_entry = self.env['time.entry'].with_context(from_analytic_line=True).create({
                'name': self.name or 'Timesheet Eintrag',
                'user_id': user.id,
                'employee_id': self.employee_id.id,
                'project_id': self.project_id.id,
                'task_id': self.task_id.id if self.task_id else False,
                'start_datetime': start_dt,
                'end_datetime': end_dt,
                'state': 'done',
                'timesheet_id': self.id,
            })
            self.env.cr.execute(
                "UPDATE account_analytic_line SET time_entry_id = %s WHERE id = %s",
                (time_entry.id, self.id)
            )
            self.invalidate_recordset(['time_entry_id'])
