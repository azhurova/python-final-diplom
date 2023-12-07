from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver, Signal
from django_rest_passwordreset.signals import reset_password_token_created

from backend.models import ConfirmEmailToken, User

__all__ = [
    'new_user_registered_signal',
    'new_order_signal',
]

new_user_registered = Signal()

new_order = Signal()


@receiver(reset_password_token_created)
def reset_password_token_created_signal(sender, instance, reset_password_token, **kwargs):
    """
    Отправляем письмо с токеном для сброса пароля
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param kwargs:
    :return:
    """

    msg = EmailMultiAlternatives(f'Password Reset Token for {reset_password_token.user}',
                                 reset_password_token.key,
                                 settings.EMAIL_HOST_USER,
                                 [reset_password_token.user.email]
                                 )
    msg.send()


@receiver(new_user_registered)
def new_user_registered_signal(user_id, **kwargs):
    """
    отправляем письмо с подтрердждением почты
    """

    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)
    msg = EmailMultiAlternatives(f'Password Reset Token for {token.user.email}',
                                 token.key,
                                 settings.EMAIL_HOST_USER,
                                 [token.user.email]
                                 )
    msg.send()


@receiver(new_order)
def new_order_signal(user_id, **kwargs):
    """
    отправяем письмо при изменении статуса заказа
    """

    user = User.objects.get(id=user_id)
    msg = EmailMultiAlternatives('Обновление статуса заказа',
                                 'Заказ сформирован',
                                 settings.EMAIL_HOST_USER,
                                 [user.email]
                                 )
    msg.send()
