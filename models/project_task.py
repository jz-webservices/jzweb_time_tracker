# -*- coding: utf-8 -*-
from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def action_timer_start(self):
        # Laufenden Time Tracker Eintrag stoppen (inkl. Timesheet-Buchung)
        running = self.env['time.entry'].search([
            ('user_id', '=', self.env.uid),
            ('state', '=', 'running'),
        ], limit=1)
        if running:
            running.action_stop()

        res = super().action_timer_start()

        # Neuen Time Tracker Eintrag starten
        employee = self.env['hr.employee'].search(
            [('user_id', '=', self.env.uid)], limit=1
        )
        if employee:
            self.env['time.entry'].create({
                'name': self.name,
                'user_id': self.env.uid,
                'employee_id': employee.id,
                'project_id': self.project_id.id if self.project_id else False,
                'task_id': self.id,
                'state': 'running',
                'start_datetime': fields.Datetime.now(),
            })
        return res

    def action_timer_stop(self):
        # Laufenden Time Tracker Eintrag für diese Aufgabe suchen
        running_entry = self.env['time.entry'].search([
            ('user_id', '=', self.env.uid),
            ('task_id', '=', self.id),
            ('state', '=', 'running'),
        ], limit=1)
        end_time = fields.Datetime.now()

        if running_entry:
            # Odoo stoppt den Timer und erstellt die analytic line —
            # from_time_tracker verhindert, dass unser Sync einen Doppeleintrag anlegt
            res = super(ProjectTask, self.with_context(from_time_tracker=True)).action_timer_stop()

            # Neu erstellte analytic line suchen und mit dem Time Tracker Eintrag verknüpfen
            new_line = self.env['account.analytic.line'].search([
                ('task_id', '=', self.id),
                ('time_entry_id', '=', False),
            ], order='id desc', limit=1)

            stop_vals = {'state': 'done', 'end_datetime': end_time}
            if new_line:
                stop_vals['timesheet_id'] = new_line.id
            running_entry.with_context(from_analytic_line=True).write(stop_vals)

            if new_line:
                new_line.with_context(from_time_tracker=True).write(
                    {'time_entry_id': running_entry.id}
                )
        else:
            # Kein laufender Time Tracker Eintrag → normaler Ablauf inkl. Sync
            res = super().action_timer_stop()

        return res
