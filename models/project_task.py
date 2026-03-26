# -*- coding: utf-8 -*-
from odoo import fields, models

RELOAD = {'type': 'ir.actions.client', 'tag': 'reload'}


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def action_timer_start(self):
        # Laufenden Time Tracker Eintrag stoppen
        running = self.env['time.entry'].search([
            ('user_id', '=', self.env.uid),
            ('state', '=', 'running'),
        ], limit=1)
        if running:
            running.action_stop()

        # Nur timer_start am Task setzen (für visuelle Anzeige) —
        # super() NICHT aufrufen, da hr_timesheet dort die "/" Live-Zeile erstellt
        self.write({'timer_start': fields.Datetime.now(), 'timer_pause': False})

        # Time Tracker Eintrag starten
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
        return RELOAD

    def action_timer_stop(self):
        # Timer-Anzeige am Task zurücksetzen
        self.write({'timer_start': False, 'timer_pause': False})

        # Laufenden Time Tracker Eintrag stoppen → erstellt Timesheet-Buchung
        running_entry = self.env['time.entry'].search([
            ('user_id', '=', self.env.uid),
            ('task_id', '=', self.id),
            ('state', '=', 'running'),
        ], limit=1)
        if running_entry:
            running_entry.action_stop()
        else:
            # Fallback falls kein Time Tracker Eintrag läuft
            super(ProjectTask, self.with_context(from_time_tracker=True)).action_timer_stop()

        return RELOAD
