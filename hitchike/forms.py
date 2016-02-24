import logging

from django import forms

from registration.forms import RegistrationForm

from hitchike.settings import ALLOWED_DOMAINS

logger = logging.getLogger(__name__)

class EmailDomainFilterRegistrationForm(RegistrationForm):

    def clean_email(self):
        submitted_data = self.cleaned_data['email']

        if not ALLOWED_DOMAINS:
            return submitted_data

        domain = submitted_data.split('@')[1]
        logger.debug(domain)
        if domain not in ALLOWED_DOMAINS:
            raise forms.ValidationError(
                u'You must register using an email address with a valid '
                'domain ({}). You can change your email address later on.'
                .format(', '.join(self.allowed_domains))
            )
        return submitted_data
