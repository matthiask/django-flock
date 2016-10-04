import json

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import ugettext as _

from flock.forms import DonationAmountForm, DonationDetailsForm
from flock.models import Project, Donation
from flock.moochers import moochers


def donate_amount(request, form_class=DonationAmountForm):
    project = Project.objects.current()

    if not project:
        return render(request, 'flock/no_project.html')

    kw = {'project': project, 'request': request}

    if request.method == 'POST':
        form = form_class(request.POST, **kw)
        if form.is_valid():
            donation = form.save()

            return redirect(
                'flock_donate_details',
                id=donation.id.hex,
            )

    else:
        form = form_class(**kw)

    return render(
        request,
        ['flock/donate_amount_form.html', 'flock/form.html'],
        {'project': project, 'form': form},
    )


def donate_details(request, id, form_class=DonationDetailsForm):
    donation = get_object_or_404(Donation, id=id)
    kw = {'instance': donation}

    try:
        kw['initial'] = json.loads(request.COOKIES['flock'])
    except:
        pass

    if request.method == 'POST':
        form = form_class(request.POST, **kw)

        if form.is_valid():
            donation = form.save()

            response = redirect(
                'flock_donate_payment_provider',
                id=donation.id.hex,
            )

            if form.cleaned_data.get('remember_my_name'):
                response.set_cookie(
                    'flock',
                    json.dumps({
                        'full_name': donation.full_name,
                        'email': donation.email,
                    }),
                )
            else:
                response.delete_cookie('flock')

            return response

    else:
        form = form_class(**kw)

    return render(
        request,
        ['flock/donate_details_form.html', 'flock/form.html'],
        {'project': donation.project, 'form': form},
    )


def donate_payment_provider(request, id):
    donation = get_object_or_404(Donation, id=id)

    if donation.charged_at is not None:
        messages.info(
            request,
            _('This donation has already been processed. Thank you!'),
        )
        return redirect('flock_donate_amount')

    return render(request, 'flock/donate_payment_provider.html', {
        'donation': donation,
        'moochers': [
            moocher.payment_form(request, donation)
            for moocher in moochers
        ],

        'thanks_url': request.build_absolute_uri(reverse('flock_thanks')),
    })


def donate_thanks(request):
    return render(request, 'flock/donate_thanks.html', {})


def donate_fail(request):
    return render(request, 'flock/donate_fail.html', {})
