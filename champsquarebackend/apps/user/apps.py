from django.urls import path
from django.contrib.auth.decorators import login_required

from django.utils.translation import gettext_lazy as _
from django.views import generic

from champsquarebackend.core.application import AppConfig
from champsquarebackend.core.loading import get_class

class UserConfig(AppConfig):
    label = 'user'
    name = 'champsquarebackend.apps.user'
    verbose_name = _('User')

    namespace = 'user'

    def ready(self):

        self.summary_view = get_class('user.views', 'AccountSummaryView')
        
        self.email_list_view = get_class('user.views', 'EmailHistoryView')
        self.email_detail_view = get_class('user.views', 'EmailDetailView')
        self.login_view = get_class('user.views', 'AccountAuthView')
        self.logout_view = get_class('user.views', 'LogoutView')
        self.register_view = get_class('user.views', 'AccountRegistrationView')
        self.profile_view = get_class('user.views', 'ProfileView')
        self.profile_update_view = get_class('user.views', 'ProfileUpdateView')
        self.profile_delete_view = get_class('user.views', 'ProfileDeleteView')
        self.change_password_view = get_class('user.views', 'ChangePasswordView')

        self.notification_inbox_view = get_class('communication.notifications.views',
                                                 'InboxView')
        self.notification_archive_view = get_class('communication.notifications.views',
                                                   'ArchiveView')
        self.notification_update_view = get_class('communication.notifications.views',
                                                  'UpdateView')
        self.notification_detail_view = get_class('communication.notifications.views',
                                                  'DetailView')

    def get_urls(self):
        urls = [
            # Login, logout and register doesn't require login
            path('login/', self.login_view.as_view(), name='login'),
            path('logout/', self.logout_view.as_view(), name='logout'),
            path('register/', self.register_view.as_view(), name='register'),
            path('', login_required(self.summary_view.as_view()),
                name='summary'),
            path('change-password/',
                login_required(self.change_password_view.as_view()),
                name='change-password'),

            # Profile
            path('profile/',
                login_required(self.profile_view.as_view()),
                name='profile-view'),
            path('profile/edit/',
                login_required(self.profile_update_view.as_view()),
                name='profile-update'),
            path('profile/delete/',
                login_required(self.profile_delete_view.as_view()),
                name='profile-delete'),

            # Email history
            path('emails/',
                login_required(self.email_list_view.as_view()),
                name='email-list'),
            path('emails/<int:email_id>/',
                login_required(self.email_detail_view.as_view()),
                name='email-detail'),

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

