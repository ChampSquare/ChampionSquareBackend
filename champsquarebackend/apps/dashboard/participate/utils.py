from django.utils.translation import gettext_lazy as _

from champsquarebackend.core.loading import get_class

Dispatcher = get_class('communication.utils', 'Dispatcher')

class ParticipantDispatcher():
    """
        Dispatcher to send concrete user related emails.
    """
    # Event codes
    QUIZ_LINK_SENT_EVENT_CODE = 'QUIZ_LINK'

    def __init__(self, logger=None, mail_connection=None):
        self.dispatcher = Dispatcher(logger=logger, mail_connection=mail_connection)

    def send_quiz_link_email_for_user(self, participant, extra_context, **kwargs):
        
        if participant.user is None:
            return 'Failed to send: No email address found'
        
        messages = self.dispatcher.get_messages(
            self.QUIZ_LINK_SENT_EVENT_CODE, extra_context
        )
        
        self.dispatcher.dispatch_user_messages(participant.user, messages)
        return _("Successfully send quiz link to %s") % participant.user.email
        