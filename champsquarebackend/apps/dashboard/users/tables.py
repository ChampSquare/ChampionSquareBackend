from django.utils.translation import gettext_lazy as _
from django_tables2 import A, Column, LinkColumn, TemplateColumn

from champsquarebackend.core.loading import get_class

DashboardTable = get_class('dashboard.tables', 'DashboardTable')


class UserTable(DashboardTable):
    check = TemplateColumn(
        template_name='champsquarebackend/dashboard/users/user_row_checkbox.html',
        verbose_name=' ', orderable=False)
    email = LinkColumn('dashboard:user-detail', args=[A('id')],
                       accessor='email')
    name = Column(accessor='get_full_name',
                  order_by=('last_name', 'first_name'))
    active = Column(accessor='is_active')
    staff = Column(accessor='is_staff')
    date_registered = Column(accessor='date_joined')
    num_orders = Column(accessor='orders__count', orderable=False, verbose_name=_('Tests Participated'))
    actions = TemplateColumn(
        template_name='champsquarebackend/dashboard/users/user_row_actions.html',
        verbose_name=' ')

    icon = "group"

    class Meta(DashboardTable.Meta):
        template_name = 'champsquarebackend/dashboard/users/table.html'

class AddUserTable(DashboardTable):
    check = TemplateColumn(
        template_name='champsquarebackend/dashboard/users/user_row_checkbox.html',
        verbose_name=' ', orderable=False)
    email = LinkColumn('dashboard:user-detail', args=[A('id')],
                       accessor='email')
    name = Column(accessor='get_full_name',
                  order_by=('last_name', 'first_name'))
    active = Column(accessor='is_active')
    date_registered = Column(accessor='date_joined')
    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='champsquarebackend/dashboard/users/user_row_actions.html',
        orderable=False)

    icon = "group"

    class Meta(DashboardTable.Meta):
        template_name = 'champsquarebackend/dashboard/users/add_user_table.html'