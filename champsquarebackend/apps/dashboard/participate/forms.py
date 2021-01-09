from django import forms
from django.utils.translation import gettext_lazy as _

from champsquarebackend.core.loading import get_class, get_model

Participant = get_model('participate', 'participant')


class ParticipantForm(forms.ModelForm):
    # start_date_time = forms.DateTimeField(
    #     widget=widgets.DateTimePickerInput(),
    #     label=_("start Date"), required=True)

    # end_date_time = forms.DateTimeField(
    #     widget=widgets.DateTimePickerInput(),
    #     label=_("End Date"), required=False)


    class Meta:
        model = Participant
        fields = ['duration', 'start_date_time', 'end_date_time',
                  'is_active', 'multiple_attempts_allowed',
                  'view_answerpaper', 'ip_restriction', 'resume_interval', 'video_monitoring_enabled']
