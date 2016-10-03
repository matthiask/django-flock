from django.conf import settings
from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy

from mooch.banktransfer import BankTransferMoocher
from mooch.mail import render_to_mail
from mooch.postfinance import PostFinanceMoocher
from mooch.signals import post_charge
from mooch.stripe import StripeMoocher

from flock.models import Donation


moochers = []
app_name = 'mooch'
urlpatterns = []

kw = {
    'model': Donation,
    'success_url': reverse_lazy('flock_thanks'),
    'failure_url': reverse_lazy('flock_fail'),
}

if getattr(settings, 'POSTFINANCE_PSPID', None):
    moocher = PostFinanceMoocher(**kw)

    moochers.append(moocher)
    urlpatterns.append(url(r'^postfinance/', include(moocher.urls)))

if getattr(settings, 'STRIPE_PUBLISHABLE_KEY', None):
    moocher = StripeMoocher(**kw)

    moochers.append(moocher)
    urlpatterns.append(url(r'^stripe/', include(moocher.urls)))

moocher = BankTransferMoocher(**kw)

moochers.append(moocher)
urlpatterns.append(url(r'^banktransfer/', include(moocher.urls)))


def send_thanks_mail(sender, payment, **kwargs):
    render_to_mail('flock/thanks_mail', {
        'donation': payment,
    }, to=[payment.email]).send(fail_silently=True)


post_charge.connect(send_thanks_mail)
