from django.conf import settings
from django.conf.urls import include, url

from mooch.banktransfer import BankTransferMoocher
from mooch.postfinance import PostfinanceMoocher
from mooch.stripe import StripeMoocher

from flock.models import Donation


moochers = []
app_name = 'mooch'
urlpatterns = []

if getattr(settings, 'POSTFINANCE_PSPID', None):
    moocher = PostfinanceMoocher(
        model=Donation,
    )

    moochers.append(moocher)
    urlpatterns.append(url(r'^postfinance/', include(moocher.urls)))

if getattr(settings, 'STRIPE_PUBLISHABLE_KEY', None):
    moocher = StripeMoocher(
        model=Donation,
    )

    moochers.append(moocher)
    urlpatterns.append(url(r'^stripe/', include(moocher.urls)))

moocher = BankTransferMoocher(
    model=Donation,
)

moochers.append(moocher)
urlpatterns.append(url(r'^banktransfer/', include(moocher.urls)))


# TODO register a signal handler for sending out the old standard THANK YOU
