from django.db import models
from django.db.models import Q

class QuoteProcessQuerySet(models.QuerySet):

    def _in_quote_docs_state(self):
        return self.filter(
            user__isnull=False,
            quoteprocessdocuments__isnull=False,
            quoteprocesspayment__isnull=True
        )

    def without_user(self):
        return self.filter(user__isnull=True)

    def quote_documents_not_uploaded(self):
        return self._in_quote_docs_state().filter(
            quoteprocessdocuments__is_submitted_for_review=False,
            quoteprocessdocuments__broker_of_record__isnull=True,
            quoteprocessdocuments__dmv_license_front_side__isnull=True,
            quoteprocessdocuments__dmv_license_back_side__isnull=True,
            quoteprocessdocuments__tlc_license_front_side__isnull=True,
            quoteprocessdocuments__tlc_license_back_side__isnull=True,
            quoteprocessdocuments__proof_of_address__isnull=True,
            quoteprocessdocuments__defensive_driving_certificate__isnull=True
        )

    def quote_documents_in_progress(self):
        return self._in_quote_docs_state().filter(
            quoteprocessdocuments__is_submitted_for_review=False
        )

    def quote_documents_submitted(self):
        return self._in_quote_docs_state().filter(
            quoteprocessdocuments__is_submitted_for_review=True
        )

    def quote_payment_done(self):
        return self.filter(
            quoteprocesspayment__payment_date__isnull=False,
            policy__isnull=True
        )

    def older_first(self):
        return self.order_by('created')