from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils.translation import ugettext_lazy as _

from champsquarebackend.core.application import AppConfig
from champsquarebackend.core.loading import get_class


class CommunicationConfig(AppConfig):
    label = 'communication'
    name = 'champsquarebackend.apps.communication'
    verbose_name = _('Communication')

    def ready(self):
        self.notification_inbox_view = get_class('communication.notifications.views', 'InboxView')
        self.notification_archive_view = get_class('communication.notifications.views', 'ArchiveView')
        self.notification_update_view = get_class('communication.notifications.views', 'UpdateView')
        self.notification_detail_view = get_class('communication.notifications.views', 'DetailView')

    def get_urls(self):
        urls = [
            # Notifications
            # Redirect to notification inbox
            path('notifications/', generic.RedirectView.as_view(
                url='/accounts/notifications/inbox/', permanent=False)),
            path('notifications/inbox/',
                login_required(self.notification_inbox_view.as_view()),
                name='notifications-inbox'),
            path('notifications/archive/',
                login_required(self.notification_archive_view.as_view()),
                name='notifications-archive'),
            path('notifications/update/',
                login_required(self.notification_update_view.as_view()),
                name='notifications-update'),
            path('notifications/<int:pk>/',
                login_required(self.notification_detail_view.as_view()),
                name='notifications-detail'),
        ]

        return self.post_process_urls(urls)


