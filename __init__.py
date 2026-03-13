from . import models


def _assign_group_to_internal_users(env):
    group = env.ref('jzweb_time_tracker.group_user', raise_if_not_found=False)
    base_group = env.ref('base.group_user', raise_if_not_found=False)
    if group and base_group:
        group.write({'users': [(4, user.id) for user in base_group.users]})


def post_init_hook(env):
    _assign_group_to_internal_users(env)


def post_update_hook(env):
    _assign_group_to_internal_users(env)
