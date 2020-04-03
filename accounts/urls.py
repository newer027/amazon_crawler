from django.contrib.auth.views import (
    logout,
    password_change,
    password_change_done,
    password_reset,
)
from django.conf.urls import url
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from .views import LoginView, UserSettingsView, SignUpView, SignUpNextView, active_user


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("没有用户使用这个邮箱!")

        return email


urlpatterns = [
    url(r'^signup/',SignUpView.as_view(),name='signup'),
    url(r'^signup_next/',SignUpNextView,name='signup_next'),
    url(r'^activate/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$',active_user,name='active_user'),
    url(r'^settings/',UserSettingsView.as_view(),name='usersettings'),
    url(r'^login/$',LoginView,name='login'),
    url(r'^logout/$',logout,{'next_page': '/accounts/login/'},name='logout'),
    url(r'^password/change/$',password_change,{'post_change_redirect': 'accounts:password_change_done'},name='password_change'),
    url(r'^password/change/done/$',password_change_done,name='password_change_done'),
    url(r'^password/reset/$',password_reset,
    {'post_reset_redirect': '/password/reset/done/',
     'html_email_template_name': 'registration/password_reset_email.html',
     'password_reset_form': EmailValidationOnForgotPassword},name='password_reset'),
]


