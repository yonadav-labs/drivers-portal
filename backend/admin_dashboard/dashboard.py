from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard

from quote.models import QuoteProcess


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for Stable.
    """

    columns = 4

    def _retrieve_email_entered(self):
        children = []
        email_entered = QuoteProcess.objects.\
            email_entered().older_first()


        for quote in email_entered:
            children.append({
                'title': str(quote),
                'url': reverse('stable_admin:quote_quoteprocess_change',  args=[quote.id] ),
            })
        
        self.children.append(modules.LinkList(
            _('Quote Process with Email Entered.'),
            draggable=False,
            deletable=False,
            collapsible=False,
            children=children,
            pre_content=("" if len(children) > 0 else "No quote process to show")
        ))
     
    def _retrieve_in_progress(self):
        children = []
        quote_documents_in_progress = QuoteProcess.objects\
            .quote_documents_in_progress().older_first()\
            .select_related('quoteprocessdocuments')

        for quote in quote_documents_in_progress:
            doc_count = quote.quoteprocessdocuments.get_documents_filled_count()
            title = f'{str(quote)} ({doc_count} documents)' if quote.user.has_usable_password() \
                else f'{str(quote)}. Password not created!'
            children.append({
                'title': title,
                'url': reverse(
                    'stable_admin:quote_quoteprocessdocuments_change',  
                    args=[quote.quoteprocessdocuments.id] ),
            })
        
        self.children.append(modules.LinkList(
            _('Quote Process with Quota Accepted.'),
            draggable=False,
            deletable=False,
            collapsible=False,
            children=children,
            pre_content=("" if len(children) > 0 else "No quote process to show")
        ))

    def _retrieve_documents_submitted(self):
        children = []
        quote_documents_submitted = QuoteProcess.objects.\
            quote_documents_submitted().older_first()\
            .select_related('quoteprocessdocuments')

        for quote in quote_documents_submitted:
            children.append({
                'title': str(quote),
                'url': reverse(
                    'stable_admin:quote_quoteprocessdocuments_change',  
                    args=[quote.quoteprocessdocuments.id] ),
            })
        
        self.children.append(modules.LinkList(
            _('Quote Process Docs Submitted for Review'),
            draggable=False,
            deletable=False,
            collapsible=False,
            children=children,
            pre_content=("" if len(children) > 0 else "No quote process to show")
        ))

    def _retrieve_payment_done(self):
        children = []
        quote_payment_done = QuoteProcess.objects.\
            quote_payment_done().older_first()

        for quote in quote_payment_done:
            children.append({
                'title': str(quote),
                'url': reverse(
                    'stable_admin:quote_quoteprocesspayment_change',  
                    args=[quote.quoteprocesspayment_id] ),
            })
        
        self.children.append(modules.LinkList(
            _('Quote Process Payment Done'),
            draggable=False,
            deletable=False,
            collapsible=False,
            children=children,
            pre_content=("" if len(children) > 0 else "No quote process to show")
        ))
   
    def init_with_context(self, context):
        self._retrieve_email_entered()
        self._retrieve_in_progress()
        self._retrieve_documents_submitted()
        self._retrieve_payment_done()

class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for hatch.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
