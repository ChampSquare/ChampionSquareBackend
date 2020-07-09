from django.core.exceptions import PermissionDenied
from django.contrib.sites.models import Site
from django.db import transaction
from django.utils.translation import gettext_lazy as _


from champsquarebackend.core.loading import get_model
from champsquarebackend.core.utils import get_ip_address, is_ip_address_valid

Participate = get_model('participate', 'Participate')
AnswerPaper = get_model('quiz', 'AnswerPaper')

class ParticipantNumberCreator(object):
    """
    Simple object for generating participant number
    """
    def participant_number(self, answerpaper):
        """
        return a participant number for a given answerpaper
        """
        return 10000 + answerpaper.id


class ParticipantCreator(object):
    """
    Create a participant by writing out the various models
    """
    def create_participant_model(self, user, quiz, answerpaper,
                                 participant_number,
                                 request, **kwargs):
        """ create a participant model"""
        participant_data = {'number': participant_number,
                            'quiz': quiz,
                            'answerpaper': answerpaper,
                            }
        if kwargs:
            participant_data.update(kwargs)
        if 'user_ip' not in participant_data:
            user_ip = get_ip_address(request)
            participant_data['user_ip'] = user_ip
        # if not is_ip_address_valid(participant_data[user_ip]):
        #     raise PermissionDenied('The ip address is not valid'
        #                             'You are not allowed to take the test')
        if user and user.is_authenticated:
            participant_data['user_id'] = user.id
        participant_data['status'] = 'created'

        if 'site' not in participant_data:
            participant_data['site'] = Site._default_manager.get_current(request)

        participate = Participate(**participant_data)
        participate.save()
        return participate

    def create_answerpaper_model(self, quiz, is_trial=False):
        answerpaper = AnswerPaper.objects.create(quiz=quiz, is_trial=is_trial)
        return answerpaper

    def start_quiz(self, quiz, request, user=None, **kwargs):
        if quiz is None or request is None:
            raise ValueError(_('quiz or request can\'t be None'))

        can_be_taken, reason = quiz.can_be_taken(request.user)

        if not can_be_taken:
            raise ValueError(_('This quiz can\'t be taken, %s' % (reason)))

        with transaction.atomic():
            answerpaper = self.create_answerpaper_model(quiz=quiz,
                                                        is_trial=user is not None \
                                                            and user.is_staff)
            participant_number = answerpaper.participant_number
            participant = self.create_participant_model(user=user,
                            quiz=quiz,
                            answerpaper=answerpaper,
                            participant_number=participant_number,
                            request=request)

        return participant






