{
    'name': 'Time Tracker',
    'version': '19.0.1.11.0',
    'category': 'Productivity',
    'summary': 'Simple start/stop time tracking with calendar view',
    'description': """
        Track your working time with a simple Start/Stop button.
        Select a project and task, start the timer – date, time and
        duration are calculated automatically. A block appears in the
        calendar for each time entry.
    """,
    'author': 'Time Tracker',
    'license': 'LGPL-3',
    'depends': ['base', 'project', 'calendar', 'hr_timesheet'],
    'data': [
        'security/time_tracker_security.xml',
        'security/ir.model.access.csv',
        'views/time_entry_search.xml',
        'views/time_entry_form.xml',
        'views/time_entry_list.xml',
        'views/time_entry_calendar.xml',
        'views/time_entry_pivot.xml',
        'views/time_entry_graph.xml',
        'views/menu.xml',
        'views/res_config_settings_views.xml',
        'views/account_analytic_line_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'jzweb_time_tracker/static/src/systray/timer_systray.js',
            'jzweb_time_tracker/static/src/systray/timer_systray.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'post_init_hook': 'post_init_hook',
    'post_update_hook': 'post_update_hook',
}
