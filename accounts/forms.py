from django import forms
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Button, Submit, Fieldset, HTML, Field
from crispy_forms.bootstrap import FormActions

from .validators import validate_email_unique, validate_username_unique


class SignUpForm(forms.Form):
    username = forms.CharField(label="用户名",max_length=30,
                               validators=[validate_username_unique])
    password = forms.CharField(label="密码",max_length=128, widget=forms.PasswordInput())
    email = forms.EmailField(label="电子邮箱",max_length=75, validators=[validate_email_unique])


    #credit = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal col-xs-12 col-md-6 col-lg-5'
        self.helper.label_class = 'col-xs-4 col-md-4 col-lg-4'
        self.helper.field_class = 'col-xs-8 col-md-8 col-lg-8'

        self. helper.layout = Layout(
            Fieldset(
                '开始创建账户',
                Field('username', autofocus=True),
                Field('password'),
                Field('email'),
            ),

    #PrependedText('prepended_text', '<input type="checkbox" checked="checked" value="" id="" name="">', active=True),
            FormActions(
                #这里的submit是设置按钮的name、value、class
                Submit('submit', '立即注册',
                       css_class='btn-success singupBtn'),
            ),
        )


class UserSettingsForm(forms.Form):
    """
    Form to allow users to change profile settings and preferences.
    """
    username = forms.CharField(required=False)
    first_name = forms.CharField(label='First Name', required=False)
    last_name = forms.CharField(label='Last Name', required=False)
    email = forms.EmailField(label='Email')
    credit = forms.IntegerField(label='积分')

    def __init__(self, *args, **kwargs):
        super(UserSettingsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal col-xs-12 col-md-6 col-lg-6'
        self.helper.label_class = 'col-xs-4 col-md-4 col-lg-4'
        self.helper.field_class = 'col-xs-8 col-md-8 col-lg-8'
        self.helper.help_text_inline = False

        self. helper.layout = Layout(
            HTML('''
            {% if messages %}
            {% for message in messages %}
            <p {% if message.tags %} class="alert alert-{{ message.tags }}"\
            {% endif %}>{{ message }}</p>{% endfor %}{% endif %}
            </p>
            '''),
            Fieldset(
                'Profile',
                Field('username', readonly=True),
                Field('credit', readonly=True),
                Field('email'),
                Field('first_name'),
                Field('last_name'),
            ),
            FormActions(
                Submit('submit', 'Save'),
                Button('cancel', 'Cancel',
                       onclick='location.href="%s";' \
                       % reverse('index')),
            ),
        )

    def clean_email(self):
        """
        Validates the email field.

        Check if the email field changed. If true, check whether the new email
        address already exists in the database and raise an error if it does.
        """
        email = self.cleaned_data['email']
        user = User.objects.get(username=self.cleaned_data['username'])

        if email.lower() != user.email.lower():
            if User.objects.filter(email__iexact=email):
                raise forms.ValidationError('Another account is already using '
                                            'this email address.')

        return email
