import json
from datetime import timedelta
from decimal import ROUND_UP
from decimal import Decimal as D

from django.contrib import messages
from django.db.models import Avg, Count, Sum
from django.template.response import TemplateResponse
from django.utils.timezone import now
from django.views.generic import TemplateView

from champsquarebackend.core.compat import get_user_model
from champsquarebackend.core.loading import get_class, get_model

RelatedFieldWidgetWrapper = get_class('dashboard.widgets', 'RelatedFieldWidgetWrapper')
User = get_user_model()
Quiz = get_model('quiz', 'quiz')
Question = get_model('question', 'question')



class IndexView(TemplateView):
    """
    An overview view which displays several reports about the shop.

    Supports the permission-based dashboard. It is recommended to add a
    :file:`champsquarebackend/dashboard/index_nonstaff.html` template because champsquarebackend's
    default template will display potentially sensitive store information.
    """

    def get_template_names(self):
        if self.request.user.is_staff:
            return ['champsquarebackend/dashboard/index.html', ]
        else:
            return ['champsquarebackend/dashboard/index_nonstaff.html', 'champsquarebackend/dashboard/index.html']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(self.get_stats())
        return ctx

    def get_quizzes(self):
        return Quiz.objects.all()

    def get_questions(self):
        return Question.objects.all()

    def get_stats(self):
        users = User.objects.all()
           
        stats = {'total_users': users.count(),
                 'total_questions': self.get_questions().count(),
                 'total_quizzes': self.get_quizzes().count()}
        
        return stats


class PopUpWindowMixin:

    @property
    def is_popup(self):
        return self.request.GET.get(
            RelatedFieldWidgetWrapper.IS_POPUP_VAR,
            self.request.POST.get(RelatedFieldWidgetWrapper.IS_POPUP_VAR))

    @property
    def is_popup_var(self):
        return RelatedFieldWidgetWrapper.IS_POPUP_VAR

    def add_success_message(self, message):
        if not self.is_popup:
            messages.info(self.request, message)


class PopUpWindowCreateUpdateMixin(PopUpWindowMixin):

    @property
    def to_field(self):
        return self.request.GET.get(
            RelatedFieldWidgetWrapper.TO_FIELD_VAR,
            self.request.POST.get(RelatedFieldWidgetWrapper.TO_FIELD_VAR))

    @property
    def to_field_var(self):
        return RelatedFieldWidgetWrapper.TO_FIELD_VAR

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if self.is_popup:
            ctx['to_field'] = self.to_field
            ctx['to_field_var'] = self.to_field_var
            ctx['is_popup'] = self.is_popup
            ctx['is_popup_var'] = self.is_popup_var

        return ctx


class PopUpWindowCreateMixin(PopUpWindowCreateUpdateMixin):

    def popup_response(self, obj):
        if self.to_field:
            attr = str(self.to_field)
        else:
            attr = obj._meta.pk.attname
        value = obj.serializable_value(attr)
        popup_response_data = json.dumps({
            'value': str(value),
            'obj': str(obj),
        })
        return TemplateResponse(
            self.request,
            'champsquarebackend/dashboard/widgets/popup_response.html',
            {'popup_response_data': popup_response_data, }
        )


class PopUpWindowUpdateMixin(PopUpWindowCreateUpdateMixin):

    def popup_response(self, obj):
        opts = obj._meta
        if self.to_field:
            attr = str(self.to_field)
        else:
            attr = opts.pk.attname
        # Retrieve the `object_id` from the resolved pattern arguments.
        value = self.request.resolver_match.kwargs['pk']
        new_value = obj.serializable_value(attr)
        popup_response_data = json.dumps({
            'action': 'change',
            'value': str(value),
            'obj': str(obj),
            'new_value': str(new_value),
        })
        return TemplateResponse(
            self.request,
            'champsquarebackend/dashboard/widgets/popup_response.html',
            {'popup_response_data': popup_response_data, }
        )


class PopUpWindowDeleteMixin(PopUpWindowMixin):

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if self.is_popup:
            ctx['is_popup'] = self.is_popup
            ctx['is_popup_var'] = self.is_popup_var

        return ctx

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL, or closes the popup, it it is one.
        """
        obj = self.get_object()

        response = super().delete(request, *args, **kwargs)

        if self.is_popup:
            obj_id = obj.pk
            popup_response_data = json.dumps({
                'action': 'delete',
                'value': str(obj_id),
            })
            return TemplateResponse(
                request,
                'champsquarebackend/dashboard/widgets/popup_response.html',
                {'popup_response_data': popup_response_data, }
            )
        else:
            return response
