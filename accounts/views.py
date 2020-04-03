import logging
from django.shortcuts import redirect,render
from django.views.generic import FormView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from axes.decorators import watch_login
from braces.views import LoginRequiredMixin
from accounts.models import UserSettings
from accounts.forms import UserSettingsForm, SignUpForm
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs, urlparse


logger = logging.getLogger(__name__)


@watch_login
def LoginView(request):
    # Force logout.
    logout(request)
    username = password = ''
    #next = None

    #if request.GET:
    #    next = request.GET['next']
    #print(next,"next")
    # Flag to keep track whether the login was invalid.
    login_failed = False

    if request.POST:
        username = request.POST['username'].replace(' ', '').lower()
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    url=parse_qs(urlparse("/"+request.META.get('HTTP_REFERER','/')).query)['next'][0]
                    return redirect(url)
                except:
                    return redirect('/')

        else:
            login_failed = True

    return render(request,'accounts/login.html',
                              {'login_failed': login_failed})


class SignUpView(FormView):
    success_url = '/accounts/signup_next'
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def get_initial(self):
        # Force logout.
        logout(self.request)

        return {'time_zone': settings.TIME_ZONE}

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.full_clean()

        if form.is_valid():
            username = form.cleaned_data['username'].replace(' ', '').lower()
            password = form.cleaned_data['password']

            user = User.objects.create(username=username)
            user.email = form.cleaned_data['email']
            user.set_password(password)
            user.is_active = False
            user.save()

            user_settings = UserSettings(user=user,credit=100)
            user_settings.save()

            logger.info('New user signed up: %s (%s)', user, user.email)

            # Automatically authenticate the user after user creation.
            #user_auth = authenticate(username=username, password=password)
            #login(request, user_auth)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class UserSettingsView(LoginRequiredMixin, FormView):
    success_url = '.'
    form_class = UserSettingsForm
    template_name = 'accounts/usersettings.html'

    def get_initial(self):
        user = self.request.user
        settings = user.settings

        return {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'credit': settings.credit,
        }

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Settings Saved!')

        return super(UserSettingsView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.full_clean()

        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            logger.info('Account Settings updated by %s', user)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

def SignUpNextView(request):
    return render(
        request,
        'accounts/signup_next.html',
    )


def active_user(request, token):
    try:
        email = token_confirm.confirm_validate_token(token)
    except:
        return render(request, 'message.html', {'message': 'expired'})
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return render(request, 'message.html', {'message': 'no_exist'})
    user.is_active = True
    user.save()
    return render(request, 'message.html', {'message': 'ok'})


from itsdangerous import URLSafeTimedSerializer as utsr
import base64
from django.conf import settings as django_settings

class Token:
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.b64encode(bytes(security_key, 'utf-8'))
    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)
    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)
    def remove_validate_token(self, token):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt)

token_confirm = Token(django_settings.SECRET_KEY)    # 定义为全局变量



def authenticate(username=None, password=None):
    if '@' in username:
        kwargs = {'email': username}
    else:
        kwargs = {'username': username}
    try:
        user = get_user_model().objects.get(**kwargs)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None