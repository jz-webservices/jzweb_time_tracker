from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    time_tracker_rounding = fields.Selection(
        [
            ('0', 'Keine Rundung'),
            ('5', '5 Minuten'),
            ('10', '10 Minuten'),
            ('15', '15 Minuten'),
            ('30', '30 Minuten'),
        ],
        string='Stoppzeit aufrunden',
        default='0',
        config_parameter='jzweb_time_tracker.rounding_minutes',
    )
