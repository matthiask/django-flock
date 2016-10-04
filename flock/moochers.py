from django.conf import settings
from django.conf.urls import include, url
from django.urls import reverse_lazy

from mooch.banktransfer import BankTransferMoocher
from mooch.mail import render_to_mail
from mooch.postfinance import PostFinanceMoocher
from mooch.signals import post_charge
from mooch.stripe import StripeMoocher

from flock.models import Donation


moochers = []
kw = {
    'model': Donation,
    'success_url': reverse_lazy('flock_thanks'),
    'failure_url': reverse_lazy('flock_fail'),
}

if getattr(settings, 'POSTFINANCE_PSPID', None):
    moochers.append(PostFinanceMoocher(
        pspid=settings.POSTFINANCE_PSPID,
        live=settings.POSTFINANCE_LIVE,
        sha1_in=settings.POSTFINANCE_SHA1_IN,
        sha1_out=settings.POSTFINANCE_SHA1_OUT,
        **kw))

if getattr(settings, 'STRIPE_PUBLISHABLE_KEY', None):
    moochers.append(StripeMoocher(
        publishable_key=settings.STRIPE_PUBLISHABLE_KEY,
        secret_key=settings.STRIPE_SECRET_KEY,
        **kw))

moochers.append(BankTransferMoocher(
    autocharge=True,
    **kw))


app_name = 'mooch'
urlpatterns = [
    url(r'', include(moocher.urls)) for moocher in moochers
]


def send_thanks_mail(sender, payment, **kwargs):
    render_to_mail('flock/thanks_mail', {
        'donation': payment,
    }, to=[payment.email]).send(fail_silently=True)


post_charge.connect(send_thanks_mail)
