from django.core.management.base import BaseCommand  

from quote.models import QuoteProcess


class Command(BaseCommand):

  help = (
      "Populate variations for all quote process"
  )

  def handle(self, *args, **kwargs):
    quotes = QuoteProcess.objects.filter(
      quoteprocessvariations__isnull=True
    )
    for quote in quotes:
      quote.set_quote_variations()
    print(f'Updated {len(quotes)} Quotes')

