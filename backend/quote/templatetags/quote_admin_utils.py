from django import template

from quote.models import QuoteProcess

register = template.Library()

@register.simple_tag(takes_context=True)
def get_quote_process(context):
  request = context.get('request')
  if request:
    quote_process_id = request.GET.get('quote_process')
    if quote_process_id:
      return QuoteProcess.objects.filter(id=quote_process_id).first()
  return None