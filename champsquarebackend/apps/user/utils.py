
from champsquarebackend.core.loading import get_class

Dispatcher = get_class('communication.utils', 'Dispatcher')
class UserDispatcher:
    """
    Dispatcher to send concrete customer related emails.
    """

    # Event codes
    REGISTRATION_EVENT_CODE = 'REGISTRATION'
    PASSWORD_RESET_EVENT_CODE = 'PASSWORD_RESET'
    PASSWORD_CHANGED_EVENT_CODE = 'PASSWORD_CHANGED'
    EMAIL_CHANGED_EVENT_CODE = 'EMAIL_CHANGED'

    def __init__(self, logger=None, mail_connection=None):
        self.dispatcher = Dispatcher(logger=logger, mail_connection=mail_connection)

    def send_registration_email_for_user(self, user, extra_context):
        messages = self.dispatcher.get_messages(self.REGISTRATION_EVENT_CODE, extra_context)
        self.dispatcher.dispatch_user_messages(user, messages)

    def send_password_reset_email_for_user(self, user, extra_context):
        messages = self.dispatcher.get_messages(self.PASSWORD_RESET_EVENT_CODE, extra_context)
        self.dispatcher.dispatch_user_messages(user, messages)

    def send_password_changed_email_for_user(self, user, extra_context):
        messages = self.dispatcher.get_messages(self.PASSWORD_CHANGED_EVENT_CODE, extra_context)
        self.dispatcher.dispatch_user_messages(user, messages)

    def send_email_changed_email_for_user(self, user, extra_context):
        messages = self.dispatcher.get_messages(
            self.EMAIL_CHANGED_EVENT_CODE, extra_context)
        self.dispatcher.dispatch_user_messages(user, messages)