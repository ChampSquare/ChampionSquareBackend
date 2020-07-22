from django.utils.translation import gettext_lazy as _

from django_tables2 import TemplateColumn, A, Column, LinkColumn

from champsquarebackend.core.loading import get_model, get_class

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
Quiz = get_model('quiz', 'quiz')
Participate = get_model('participate', 'participate')

class QuizTable(DashboardTable):
    name = Column(
        verbose_name=_('Name'),
        orderable=False, accessor=('name'))

    category = Column(
        verbose_name=_('Category'),
        orderable=False, accessor=('category'))

    total_marks = Column(
        verbose_name=_('Marks'),
        orderable=False, accessor=('total_marks'))

    questions = TemplateColumn(
        verbose_name=_('Questions'),
        template_name='champsquarebackend/dashboard/quiz/quiz_row_questions.html',
        orderable=False)

    users = TemplateColumn(
        verbose_name=_('Users'),
        template_name='champsquarebackend/dashboard/quiz/quiz_row_users.html',
        orderable=False)

    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='champsquarebackend/dashboard/quiz/quiz_row_actions.html',
        orderable=False)

    icon = "sitemap"

    class Meta(DashboardTable.Meta):
        model = Quiz
        fields = ()
        sequence = ('counter', 'name', 'questions', 'total_marks', 'users', 'category', 'actions')


class UserTable(DashboardTable):
    check = TemplateColumn(
        template_name='champsquarebackend/dashboard/quiz/user_row_checkbox.html',
        verbose_name=' ', orderable=False)
    email = LinkColumn('dashboard:user-detail', args=[A('id')],
                       accessor='email')
    name = Column(accessor='get_full_name',
                  order_by=('last_name', 'first_name'))
    active = Column(accessor='is_active')
    date_registered = Column(accessor='date_joined')

    icon = "group"

    class Meta(DashboardTable.Meta):
        template_name = 'champsquarebackend/dashboard/quiz/add_user_table.html'


class ParticipantTable(DashboardTable):
    check = TemplateColumn(
        template_name='champsquarebackend/dashboard/quiz/participant_row_checkbox.html',
        verbose_name=' ', orderable=False)
    
    name = Column(
        verbose_name=_('Name'),
        orderable=False, accessor=('full_name')
    )

    attempt = Column(
        verbose_name=_('Attempted?'),
        orderable=False, accessor=('has_taken_quiz')
    )

    start_time = Column(
        verbose_name=_('Start Time'),
        orderable=False, accessor=('get_start_time')
    )

    end_time = Column(
        verbose_name=_('End Time'),
        orderable=False, accessor=('get_end_time')
    )

    icon = "group"

    class Meta(DashboardTable.Meta):
        template_name = 'champsquarebackend/dashboard/quiz/participant_table.html'