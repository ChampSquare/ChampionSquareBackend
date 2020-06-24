from django import forms
from .models import get_model_class, Profile, Quiz, Question, Course,\
                         QuestionPaper
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from textwrap import dedent
try:
    from string import letters
except ImportError:
    from string import ascii_letters as letters
from string import punctuation, digits
import datetime
import pytz
from django.template import Template
# from material import Layout, Row, Column, Fieldset, Span2, Span3, Span5, Span6, Span10



# from . import Uscholar as forms
from champsquarebackend.legacy.Unicorn.models import Student



subjects = (
       ("select", "Select Language"),
       ("physics", "Physics"),
       ("chemistry", "Chemistry"),
       ("mathematics", "Mathematics"),
       ("biology", "Biology"),
   )


question_types = (
    ("select", "Select Question Type"),
    ("mcq", "Multiple Choice"),
    ("mcc", "Multiple Correct Choices"),
    ("integer", "Answer in Integer"),
    ("paragraph", "Paragraph Type"),
    ("match", "Matching Type")
    )

test_case_types = (
        ("mcqtestcase", "MCQ Testcase"),
        ("integertestcase", "Integer Testcase"),
        )



UNAME_CHARS = letters + "._" + digits
PWD_CHARS = letters + punctuation + digits

attempts = [(i, i) for i in range(1, 6)]
attempts.append((-1, 'Infinite'))
days_between_attempts = ((j, j) for j in range(401))

def get_object_form(model, exclude_fields=None):
    model_class = get_model_class(model)
    class _ObjectForm(forms.ModelForm):
        class Meta:
            model = model_class
            exclude = exclude_fields
    return _ObjectForm


class AddUserForm(forms.Form):
    roll_number = forms.CharField \
        (max_length=30, help_text="Use a dummy if you don't have one.")
    name = forms.CharField(max_length=30)

    phone_number = forms.CharField(max_length=15)  # validators should be a list
    batch = forms.CharField(max_length=30)

    def clean_username(self):
        u_name = self.cleaned_data["roll_number"]
        if u_name.strip(UNAME_CHARS):
            msg = "Only letters, digits, period and underscore characters are"\
                  " allowed in username"
            raise forms.ValidationError(msg)
        try:
            User.objects.get(username__exact=u_name)
            raise forms.ValidationError("Username already exists.")
        except User.DoesNotExist:
            return u_name

    def save(self):
        u_name = self.cleaned_data["roll_number"]
        roll_number = self.cleaned_data["roll_number"]
        name = self.cleaned_data["name"]
        pwd = self.cleaned_data["phone_number"]
        phone_number = self.cleaned_data["phone_number"]
        batch = self.cleaned_data["batch"]
        email = "ujjawal@example.com"
        new_user = User.objects.create_user(u_name, email, pwd)
        new_student = Student(roll_number=roll_number, name=name, batch=batch, mobile_number=phone_number)
        new_student.save()

        new_profile = Profile(user=new_user, student=new_student, pwd=pwd)

        new_profile.save()

        return u_name, pwd





class UserRegisterForm(forms.Form):
    """A Class to create new form for User's Registration.
    It has the various fields and functions required to register
    a new user to the system"""

    username = forms.CharField(max_length=30, help_text='Letters, digits,\
                period and underscores only.')
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    confirm_password = forms.CharField\
                       (max_length=30, widget=forms.PasswordInput(), label="Confirm password")
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    roll_number = forms.CharField\
                (max_length=30, help_text="Use a dummy if you don't have one.")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Enter your phone number")
    phone_number = forms.CharField(validators=[phone_regex], max_length=17)  # validators should be a list

    institute = forms.CharField \
        (max_length=128, help_text='Institute/Organization')

    # layout = Layout('username', 'email',
    #                 Row('password', 'confirm_password'),
    #                 Fieldset('Pesonal details',
    #                          Row('first_name', 'last_name'),
    #                          Row('roll_number', 'phone_number'),
    #                          Row('institute')))

    # template = Template("""
    # {% form %}
    #     {% part form.username prefix %}<i class="material-icons prefix">account_box</i>{% endpart %}
    #     {% part form.email prefix %}<i class="material-icons prefix">email</i>{% endpart %}
    #     {% part form.password prefix %}<i class="material-icons prefix">lock_open</i>{% endpart %}
    # {% endform %}  \
    # """)

    # buttons = Template("""
    #     <button class="waves-effect waves-light btn" type="submit">Submit</button>
    # """)

    title = "Registration form"

    def clean_username(self):
        u_name = self.cleaned_data["username"]
        if u_name.strip(UNAME_CHARS):
            msg = "Only letters, digits, period and underscore characters are"\
                  " allowed in username"
            raise forms.ValidationError(msg)
        try:
            User.objects.get(username__exact=u_name)
            raise forms.ValidationError("Username already exists.")
        except User.DoesNotExist:
            return u_name

    def clean_password(self):
        pwd = self.cleaned_data['password']
        if pwd.strip(PWD_CHARS):
            raise forms.ValidationError("Only letters, digits and punctuation\
                                        are allowed in password")
        return pwd

    def clean_confirm_password(self):
        c_pwd = self.cleaned_data['confirm_password']
        pwd = self.data['password']
        if c_pwd != pwd:
            raise forms.ValidationError("Passwords do not match")

        return c_pwd

    def save(self):
        u_name = self.cleaned_data["username"]
        u_name = u_name.lower()
        pwd = self.cleaned_data["password"]
        email = self.cleaned_data['email']
        new_user = User.objects.create_user(u_name, email, pwd)

        new_user.first_name = self.cleaned_data["first_name"]
        new_user.last_name = self.cleaned_data["last_name"]
        new_user.save()

        cleaned_data = self.cleaned_data
        new_profile = Profile(user=new_user)
        new_profile.roll_number = cleaned_data["roll_number"]
        new_profile.phone_number = cleaned_data["phone_number"]
        new_profile.institute = cleaned_data["institute"]

        new_profile.save()

        return u_name, pwd


class UserLoginForm(forms.Form):
    """Creates a form which will allow the user to log into the system."""

    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())

    def clean(self):
        super(UserLoginForm, self).clean()
        try:
            u_name, pwd = self.cleaned_data["username"],\
                          self.cleaned_data["password"]
            user = authenticate(username=u_name, password=pwd)
        except Exception:
            raise forms.ValidationError\
                        ("Username and/or Password is not entered")
        if not user:
            raise forms.ValidationError("Invalid username/password")
        return user


class QuizForm(forms.ModelForm):
    """Creates a form to add or edit a Quiz.
    It has the related fields and functions required."""

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        course_id = kwargs.pop('course')
        super(QuizForm, self).__init__(*args, **kwargs)
        self.fields['prerequisite'] = forms.ModelChoiceField(
                queryset=Quiz.objects.filter(course__id=course_id,
                                             is_trial=False))
        self.fields['prerequisite'].required = False
        self.fields['course'] = forms.ModelChoiceField(
                queryset=Course.objects.filter(id=course_id), empty_label=None)

    class Meta:
        model = Quiz
        exclude = []


class QuestionForm(forms.ModelForm):
    """Creates a form to add or edit a Question.
    It has the related fields and functions required."""

    class Meta:
        model = Question
        exclude = ['user', 'active']


class QuestionFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(QuestionFilterForm, self).__init__(*args, **kwargs)
        questions = Question.objects.filter(user_id=user.id)
        points_list = questions.values_list('points', flat=True).distinct()
        points_options = [(None, 'Select Marks')]
        points_options.extend([(point, point) for point in points_list])
        self.fields['marks'] = forms.FloatField(widget=forms.Select\
                                                    (choices=points_options))

    subject = forms.CharField(max_length=8, widget=forms.Select\
                                (choices=subjects))
    question_type = forms.CharField(max_length=8, widget=forms.Select\
                                    (choices=question_types))


class CourseForm(forms.ModelForm):
    """ course form for moderators """

    class Meta:
        model = Course
        exclude = ['creator', 'requests', 'students', 'rejected',
            'created_on', 'is_trial', 'teachers']


class ProfileForm(forms.ModelForm):
    """ profile form for students and moderators """

    class Meta:
        model = Profile
        fields = ['first_name', 'picture', 'last_name']

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name


class QuestionPaperForm(forms.ModelForm):
    class Meta:
        model = QuestionPaper
        fields = []


class UploadFileForm(forms.Form):
    file = forms.FileField()


