from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from asin_keyword.emails import send_email
from django.conf import settings as django_settings
from itsdangerous import URLSafeTimedSerializer as utsr
import base64


def validate_email_unique(value):
    exists = User.objects.filter(email__iexact=value)

    if exists:
        raise ValidationError('Someone is already using this email address. '
                              'Please try another.')
    else:
        token = token_confirm.generate_validate_token(value)
        message = "\n".join([u'尊敬的用户,欢迎加入AMZ668.COM', u'请访问该链接，完成用户验证:',
        '/'.join(['amz668.com/accounts/activate',token])])
        try:
            send_email(value, message, '激活AMZ668账号')
        except:
            raise ValidationError('验证邮件发送失败,请重新填写邮箱.')

def validate_username_unique(value):
    exists = User.objects.filter(username__iexact=value)
    invalid_usernames = [
        'glucosetracker',
        'glucose',
        'diabetes',
        'admin',
        'help',
        'helpdesk',
        'sales',
        'support',
        'info',
        'warning',
        'success',
        'danger',
        'error',
        'debug',
        'alert',
        'alerts',
        'signup',
        'signin',
        'signout',
        'login',
        'logout',
        'activate',
        'register',
        'password',
    ]

    if exists or value in invalid_usernames:
        raise ValidationError('This username is not available. '
                              'Please try another.')

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
        print(serializer.loads(token, salt=self.salt))
        return serializer.loads(token, salt=self.salt)

token_confirm = Token(django_settings.SECRET_KEY)