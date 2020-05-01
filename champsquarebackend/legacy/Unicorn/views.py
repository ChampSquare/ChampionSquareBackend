from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
import random
import string
from django.db.models import Sum, Max, Q, F


from .models import OfflineExamResult, OfflineExam, OfflineResult, Student
from .forms import OfflineResultForm,  ConfirmImportForm, EnterRollNumberForm, TokenForm
from .tmp_storage import TempFolderStorage, CacheStorage

from authy.api import AuthyApiClient

from champsquarebackend.legacy.Uscholar.models import Profile, Course


URL_ROOT = ''
TMP_STORAGE_CLASS = getattr(settings, 'TMP_STORAGE_CLASS',
                            TempFolderStorage)

tmp_storage_class = None
authy_api = AuthyApiClient(settings.ACCOUNT_SECURITY_API_KEY)


def my_render_to_response(template, context=None, **kwargs):
    """Overridden render.
    """
    if context is None:
        context = {'URL_ROOT': URL_ROOT}
    else:
        context['URL_ROOT'] = URL_ROOT
    return render(template, context, **kwargs)


def home(request):
    user = request.user
    courses = Course.objects.filter(active=True, is_trial=False)
    title = 'All Courses'
    context = {'user': user, 'courses': courses, 'title': title}

    # if request.method == 'GET':
    #     form = ContactForm()
    # else:
    #     form = ContactForm(request.POST)
    #     if form.is_valid():
    #         from_name = form.cleaned_data['contact_name']
    #         from_email = form.cleaned_data['contact_email']
    #         from_mobile_number = form.cleaned_data['contact_mobile']
    #         message = form.cleaned_data['content']
    #         msg_plain = render_to_string('contact_template.txt', {'contact_name': from_name, 'contact_mobile': from_mobile_number,
    #                                                              'contact_email': from_email, 'contact_content': message})
    #         try:
    #             send_mail("Target IITJEE", msg_plain, from_email, ['contact@targetiitjeeclasses.org'])
    #         except BadHeaderError:
    #             return HttpResponse('Invalid header found.')
    #         return redirect('/')

    # context = {'form': form}
    return render(request, 'Unicorn/home.html', context)


def see_result(request):
    """ search offline result """
    ci = RequestContext(request)

    context = {}
    results = []

    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        if not len(roll_number) == 0:
            for result in OfflineExamResult.objects.all():
                if result.roll_number == roll_number:
                    results.append(result)

            # results = OfflineExamResult.objects.annotate(roll_number=F('uid1') + F('uid2'))\
            # .filter(roll_number=identifier)
            context['success'] = True
            context['results'] = results
    return render(request, 'Unicorn/seeresult.html', context)


def get_user_detail(request):
    context = {'success': False, 'student': None}
    if request.method == 'POST':
        form = EnterRollNumberForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['roll_number']
            if Student.objects.filter(roll_number=number).exists():
                student = Student.objects.get(roll_number=number)
                context['student'] = student
                request.session['phone_number'] = student.mobile_number
                request.session['country_code'] = '+91'
                request.session['roll_number'] = number
                authy_api.phones.verification_start(
                    student.mobile_number,
                    '+91',
                       via=form.cleaned_data['via']
                )
                return redirect('/verification/')
            else:
                context['roll_number'] = number
                form.add_error('roll_number', 'No Student found with this roll number.\
                             Please contact Jupiter Office')
                context['form'] = form
                return render(request, 'Unicorn/registration_new.html', context)
    context["form"] = EnterRollNumberForm
    return render(request, 'Unicorn/registration_new.html', context)


def token_validation(request):
    if request.method == 'POST':
        form = TokenForm(request.POST)
        if form.is_valid():
            verification = authy_api.phones.verification_check(
                request.session['phone_number'],
                request.session['country_code'],
                form.cleaned_data['token']
            )
            if verification.ok():
                request.session['is_verified'] = True
                username = request.session['roll_number']

                if not User.objects.filter(username=username).exists():
                    pwd = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
                    new_user = User.objects.create_user(username, "ujjawal@example.com", pwd)
                    new_user.save()
                    new_profile = Profile(user=new_user)
                    new_profile.student = Student.objects.get(roll_number=username)
                    new_profile.pwd = pwd
                    new_profile.save()
                    user = authenticate(username=username, password=pwd)

                else:
                    user = User.objects.get(username=username)
                    pwd = user.profile.pwd
                    user = authenticate(username=username, password=pwd)

                login(request, user)

                return redirect('/')
            else:
                for error_msg in verification.errors().values():
                    form.add_error(None, error_msg)
    else:
        form = TokenForm()
    return render(request, 'Unicorn/token_validation.html', {'form': form})


def verified(request):
    if not request.session.get('is_verified'):
        return redirect('phone_verification')
    return render(request, 'verified.html')


def contact(request):
    from_name = request.POST.get('name', None)
    from_email = request.POST.get('email', "user@example.com")
    from_mobile_number = request.POST.get('phone', None)
    message = request.POST.get('message', None)
    msg_plain = render_to_string('contact_template.txt',
                                 {'contact_name': from_name, 'contact_mobile': from_mobile_number,
                                  'contact_email': from_email, 'contact_content': message})
    try:
        send_mail("Jupiter", msg_plain, from_email, ['ujjawalanand1729@gmail.com'])
    except BadHeaderError:
        data = {
            'success': False,
            'message': "Bad Header Request"
        }
        return JsonResponse(data)

    data = {
        'success': True,
        'message': "Message sent successfully! \nThanks for contacting us, we will contact you back!"
    }
    return JsonResponse(data)
