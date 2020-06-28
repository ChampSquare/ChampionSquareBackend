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
        # ctx.update(self.get_stats())
        return ctx

    
    # def get_hourly_report(self, orders, hours=24, segments=10):
    #     """
    #     Get report of order revenue split up in hourly chunks. A report is
    #     generated for the last *hours* (default=24) from the current time.
    #     The report provides ``max_revenue`` of the hourly order revenue sum,
    #     ``y-range`` as the labelling for the y-axis in a template and
    #     ``order_total_hourly``, a list of properties for hourly chunks.
    #     *segments* defines the number of labelling segments used for the y-axis
    #     when generating the y-axis labels (default=10).
    #     """
    #     # Get datetime for 24 hours ago
    #     time_now = now().replace(minute=0, second=0)
    #     start_time = time_now - timedelta(hours=hours - 1)

    #     order_total_hourly = []
    #     for hour in range(0, hours, 2):
    #         end_time = start_time + timedelta(hours=2)
    #         hourly_orders = orders.filter(date_placed__gte=start_time,
    #                                       date_placed__lt=end_time)
    #         total = hourly_orders.aggregate(
    #             Sum('total_incl_tax')
    #         )['total_incl_tax__sum'] or D('0.0')
    #         order_total_hourly.append({
    #             'end_time': end_time,
    #             'total_incl_tax': total
    #         })
    #         start_time = end_time

    #     max_value = max([x['total_incl_tax'] for x in order_total_hourly])
    #     divisor = 1
    #     while divisor < max_value / 50:
    #         divisor *= 10
    #     max_value = (max_value / divisor).quantize(D('1'), rounding=ROUND_UP)
    #     max_value *= divisor
    #     if max_value:
    #         segment_size = (max_value) / D('100.0')
    #         for item in order_total_hourly:
    #             item['percentage'] = int(item['total_incl_tax'] / segment_size)

    #         y_range = []
    #         y_axis_steps = max_value / D(str(segments))
    #         for idx in reversed(range(segments + 1)):
    #             y_range.append(idx * y_axis_steps)
    #     else:
    #         y_range = []
    #         for item in order_total_hourly:
    #             item['percentage'] = 0

    #     ctx = {
    #         'order_total_hourly': order_total_hourly,
    #         'max_revenue': max_value,
    #         'y_range': y_range,
    #     }
    #     return ctx

    # def get_stats(self):
    #     datetime_24hrs_ago = now() - timedelta(hours=24)
    #     customers = User.objects.filter(orders__isnull=False).distinct()
       
    #     user = self.request.user
    #     if not user.is_staff:
    #         partners_ids = tuple(user.partners.values_list('id', flat=True))
            
    #         customers = customers.filter(
    #             orders__lines__partner_id__in=partners_ids
    #         ).distinct()
           
    #     stats = {'total_customers': customers.count()}
        
    #     return stats


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