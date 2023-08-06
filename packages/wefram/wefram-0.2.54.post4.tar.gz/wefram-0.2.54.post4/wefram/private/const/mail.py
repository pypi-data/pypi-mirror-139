from ...urls import asset_url
from ...l10n import lazy_gettext


__all__ = [
    'APP_ICON',
    'MSG_APP_CAPTION',
    'MSG_PERMISSION',
    'PERMISSION'
]

APP_ICON = asset_url('icons/mail-accounts.png')

MSG_APP_CAPTION = lazy_gettext("Mails", 'system.mail')
MSG_PERMISSION = lazy_gettext("Administer mails", 'system.mail')

PERMISSION = 'adminMail'
