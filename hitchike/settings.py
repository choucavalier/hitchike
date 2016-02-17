from split_settings.tools import optional, include

include(
    'settings/base.py',
    'settings/database.py',
    optional('settings/local.py'),

    scope=globals()
)
