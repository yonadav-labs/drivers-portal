from quote.models import QuoteProcessPayment

class SendQuoteProcessPayment(QuoteProcessPayment):

  class Meta:
    proxy=True