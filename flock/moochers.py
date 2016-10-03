from django.conf import settings
from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy

from mooch.banktransfer import BankTransferMoocher
from mooch.postfinance import PostfinanceMoocher
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
    moocher = PostfinanceMoocher(**kw)

    moochers.append(moocher)
    urlpatterns.append(url(r'^postfinance/', include(moocher.urls)))

if getattr(settings, 'STRIPE_PUBLISHABLE_KEY', None):
    moocher = StripeMoocher(**kw)

    moochers.append(moocher)
    urlpatterns.append(url(r'^stripe/', include(moocher.urls)))

moocher = BankTransferMoocher(**kw)

moochers.append(moocher)
urlpatterns.append(url(r'^banktransfer/', include(moocher.urls)))


# TODO register a signal handler for sending out the old standard THANK YOU
