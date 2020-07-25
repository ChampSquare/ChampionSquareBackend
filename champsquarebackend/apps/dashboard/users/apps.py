from django.urls import path
from django.utils.translation import gettext_lazy as _

from champsquarebackend.core.application import AppDashboardConfig
from champsquarebackend.core.loading import get_class


class UsersDashboardConfig(AppDashboardConfig):
    label = 'users_dashboard'
    name = 'champsquarebackend.apps.dashboard.users'
    verbose_name = _('Users dashboard')

    default_permissions = ['is_staff', ]

    def ready(self):
        self.user_list_view= get_class('dashboard.users.views', 'UserListView')
        self.user_detail_view = get_class('dashboard.users.views', 'UserDetailView')
        self.password_reset_view = get_class('dashboard.users.views',
                                             'PasswordResetView')
        self.add_user_view = get_class('dashboard.users.views', 'AddUserToQuizView')
        self.user_create_update_view = get_class('dashboard.users.views', 'UserCreateUpdateView')
        
        
    def get_urls(self):
        urls = [
            path('', self.user_list_view.as_view(), name='users-index'),
            path('<int:pk>/',
                self.user_detail_view.as_view(), name='user-detail'),
            path('<int:pk>/password-reset/',
                self.password_reset_view.as_view(),
                name='user-password-reset'),
            path('quiz/<int:pk>/add/', self.add_user_view.as_view(), name='quiz-add-user'),
            path('create/', self.user_create_update_view.as_view(), name='user-create'),
            path('<int:pk>/update/', self.user_create_update_view.as_view(), name='user-update')
            
        ]
        return self.post_process_urls(urls)
