from django.conf.urls import include, url

from flock import views


urlpatterns = [
    url(
        r'^$',
        views.donate_amount,
        name='flock_donate_amount',
    ),
    url(
        r'^details/(?P<id>[a-z0-9\-]+)/$',
        views.donate_details,
        name='flock_donate_details',
    ),
    url(
        r'^psp/(?P<id>[a-z0-9\-]+)/$',
        views.donate_payment_provider,
        name='flock_donate_payment_provider',
    ),

    url(r'', include('flock.moochers', namespace='mooch')),

    url(
        r'^thanks/$',
        views.donate_thanks,
        name='flock_thanks',
    ),

    url(
        r'^fail/$',
        views.donate_fail,
        name='flock_fail',
    ),
]
