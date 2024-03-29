from django.core.exceptions import PermissionDenied
from django.contrib.sites.models import Site
from django.db import transaction
from django.utils.translation import gettext_lazy as _


from champsquarebackend.core.loading import get_model
from champsquarebackend.core.utils import get_ip_address, is_ip_address_valid

Participant = get_model('participate', 'Participant')
AnswerPaper = get_model('quiz', 'AnswerPaper')
Answer = get_model('quiz', 'Answer')

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
    def create_or_update_participant(self, quiz, request,
                                 participant, **kwargs):
        """ create a participant model"""
        user = request.user
        participant_data = {}
        if participant is None:
            participant_data = {'quiz': quiz,
                                'user': user,
                                'is_active': True}
            participant = Participant(**participant_data)
            participant.save()

        participant.site = Site._default_manager.get_current(request)
        participant.save()
        return participant

    def create_answerpaper_model(self, quiz, participant, request, is_trial=False):
        # answerpapers are ordered by '-created_at', so the first one is the most recent one
        answerpaper = AnswerPaper.objects.filter(participant=participant.id).first()
        # todo : check for resume conditions
        if answerpaper is not None and not answerpaper.is_closed:
            return answerpaper
        answerpaper = AnswerPaper.objects.create(quiz=quiz,
                                                 participant=participant,
                                                 is_trial=is_trial,
                                                 user_ip=get_ip_address(request),
                                                 status='created')
        questions = answerpaper.quiz.questionpaper.questions.all()
        # create empty answers for all questions in questionpaper as well
        Answer.objects.bulk_create([Answer(question=question, answerpaper=answerpaper)
                                            for question in questions])
        return answerpaper

    def start_quiz(self, quiz, request, participant, **kwargs):
        if quiz is None or request is None:
            raise ValueError(_('quiz or request can\'t be None'))

        with transaction.atomic():
            participant = self.create_or_update_participant(quiz=quiz,
                            request=request, participant=participant, **kwargs)
            answerpaper = self.create_answerpaper_model(quiz=quiz, participant=participant, request=request)
                                                        # is_trial=request.user is not None \
                                                            # and request.user.is_staff)
            

        return answerpaper






