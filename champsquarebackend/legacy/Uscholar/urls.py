from django.urls import path
from . import views
from . import forms
from django.views import generic

app_name = "Uscholar"

urlpatterns = [
    # path('', views.index),
    path('', views.user_login, name='login'),
    path('home/', views.homepage, name='homepage'),
    path('instructions/', views.instructions, name='instructions'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('quizzes/', views.quizlist_user, name='quizlist_user'),
    path('quizzes/<int:enrolled>/', views.quizlist_user, name='quizlist_user'),
    path('results/', views.results_user),
    path('start/', views.start),
    path('start/<int:questionpaper_id>/', views.start),
    path('start/<int:attempt_num>/<int:questionpaper_id>/', views.start),
    # path('quit/<int:attempt_num>/<int:questionpaper_id>/', views.quit),
    path('complete/', views.complete),
    path('complete/<int:attempt_num>/<int:questionpaper_id>/',\
            views.complete),
    path('register/', views.user_register),
    path('download_result/', views.download_csv, name='result download'),
    
    path('download_paper/<str:username>/', views.download_answer_paper, name='paper save'),

    path('enroll_request/<int:course_id>/', views.enroll_request, name='enroll_request'),
    path('self_enroll/<int:course_id>/', views.self_enroll, name='self_enroll'),
    path('view_answerpaper/<int:questionpaper_id>/', views.view_answerpaper, name='view_answerpaper'),
    path('manage/', views.prof_manage, name='manage'),
    path('manage/show_result/', views.show_results, name='show_result'),
    path('manage/show_result/<int:questionpaper_id>/', views.show_results, name='show_result'),

    path('manage/addquestion/', views.add_question),
    path('manage/addquestion/<int:question_id>/', views.add_question),
    path('manage/addquiz/<int:course_id>/', views.add_quiz, name='add_quiz'),
    path('manage/addquiz/<int:course_id>/<int:quiz_id>/', views.add_quiz, name='edit_quiz'),
    path('manage/gradeuser/', views.grade_user),
    path('manage/gradeuser/<int:quiz_id>/',views.grade_user),
    path('manage/gradeuser/<int:quiz_id>/<int:user_id>/',views.grade_user),
    path('manage/gradeuser/<int:quiz_id>/<int:user_id>/<int:attempt_number>/',views.grade_user),
    path('manage/questions/', views.show_all_questions),
    path('manage/monitor/', views.monitor),
    path('manage/add_user/', views.add_user),
    path('manage/showquestionpapers/', views.show_all_questionpapers),
    path('manage/showquestionpapers/<int:questionpaper_id>/',\
                                                    views.show_all_questionpapers),
    
    
    path('manage/show_students/', views.show_students),
    path('manage/monitor/<int:questionpaper_id>/', views.monitor),
    path('manage/user_data/<int:user_id>/<int:questionpaper_id>/',
        views.user_data),
    path('manage/user_data/<int:user_id>/', views.user_data),
    path('manage/quiz/designquestionpaper/<int:quiz_id>/', views.design_paper,
        name='design_questionpaper'),
    path('manage/designquestionpaper/<int:quiz_id>/<int:questionpaper_id>/',
        views.design_paper, name='designquestionpaper'),
    path('manage/statistics/question/<int:questionpaper_id>/',
        views.show_statistics),
    
    
    path('manage/statistics/question/<int:questionpaper_id>/<int:attempt_number>/',
        views.show_statistics),
    path('manage/monitor/download_csv/<int:questionpaper_id>/',
        views.download_csv),
    path('manage/courses/', views.courses, name='courses'),
    path('manage/add_course/', views.add_course, name='add_course'),
    path('manage/edit_course/<int:course_id>', views.add_course, name='edit_course'),
    path('manage/course_detail/<int:course_id>/', views.course_detail, name='course_detail'),
    path('manage/enroll/<int:course_id>/<int:user_id>/', views.enroll),
    path('manage/enroll/rejected/<int:course_id>/<int:user_id>/',
        views.enroll, {'was_rejected': True}),
    
    path('manage/reject/<int:course_id>/<int:user_id>/', views.reject),
    path('manage/enrolled/reject/<int:course_id>/<int:user_id>/',
        views.reject, {'was_enrolled': True}),
    path('manage/toggle_status/<int:course_id>/', views.toggle_course_status),
    path('ajax/questions/filter/', views.ajax_questions_filter),
    path('editprofile/', views.edit_profile, name='edit_profile'),
    path('viewprofile/', views.view_profile, name='view_profile'),
    path('manage/enroll/<int:course_id>/', views.enroll),
    path('manage/enroll/rejected/<int:course_id>/',
        views.enroll, {'was_rejected': True}),
    path('manage/enrolled/reject/<int:course_id>/',
        views.reject, {'was_enrolled': True}),
    path('manage/searchteacher/<int:course_id>/', views.search_teacher),
    
    
    path('manage/addteacher/<int:course_id>/', views.add_teacher, name='add_teacher'),
    path('manage/remove_teachers/<int:course_id>/', views.remove_teachers, name='remove_teacher'),
    path('manage/download_questions/', views.show_all_questions),
    path('manage/upload_questions/', views.show_all_questions),
    path('manage/grader/', views.grader, name='grader'),
    path('manage/regrade/question/<int:course_id>/<int:question_id>/',
            views.regrade, name='regrade'),
    path('manage/regrade/questionpaper/<int:course_id>/<int:question_id>/<int:questionpaper_id>/',
            views.regrade, name='regrade'),
    
    path('manage/regrade/answerpaper/<int:course_id>/<int:question_id>/<int:answerpaper_id>/',
            views.regrade, name='regrade'),
    path('manage/regrade/paper/<int:course_id>/<int:answerpaper_id>/',
            views.regrade, name='regrade'),
    
    path('manage/<str:mode>/<int:quiz_id>/', views.test_quiz),
    
    
    path('manage/create_demo_course/', views.create_demo_course),
    path('manage/courses/download_course_csv/<int:course_id>/',
        views.download_course_csv),

    #path('register/', generic.FormView.as_view(
    #    form_class=forms.UserRegisterForm, success_url='/login/', template_name="Uscholar/register_material.html")),
    # path('<int:q_id>/check/', views.check),
    # path('<int:q_id>/clear_response/<int:attempt_num>/<int:questionpaper_id>/',\
    #         views.clear_response),
    # path('<int:q_id>/mark_for_review_and_next/<int:attempt_num>/<int:questionpaper_id>/',\
    #         views.mark_for_review_and_next),
    # path('<int:q_id>/check/<int:attempt_num>/<int:questionpaper_id>/',\
    #         views.check),
    # path('<int:q_id>/skip/<int:attempt_num>/<int:questionpaper_id>/',
    #     views.skip),
    # path('<int:q_id>/skip_section/<int:section>.+)/<int:attempt_num>/<int:questionpaper_id>/',
    #     views.skip_section),
    # path('<int:q_id>/skip/<int:next_q>/<int:attempt_num>/<int:questionpaper_id>/',
    #     views.skip),
]
