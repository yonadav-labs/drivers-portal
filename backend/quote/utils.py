from quote.constants import (
  QUOTE_PROCESS_DEDUCTIBLE_750, QUOTE_PROCESS_DEDUCTIBLE_1000, QUOTE_PROCESS_DEDUCTIBLE_1500,
    QUOTE_STATUS_CREATED, QUOTE_STATUS_DOCS, QUOTE_STATUS_REVIEW, QUOTE_STATUS_PAYMENT, 
    QUOTE_STATUS_PAID, QUOTE_STATUS_DONE, HEREFORD_FEES
)

def get_quote_status(quote_process):
  docs = quote_process.quote_process_documents
  if not docs:
    return QUOTE_STATUS_CREATED
  
  if not docs.is_submitted_for_review:
    return QUOTE_STATUS_DOCS
  
  payment = quote_process.quote_process_payment
  if not payment:
    return QUOTE_STATUS_REVIEW
  
  if not payment.is_paid:
    return QUOTE_STATUS_PAYMENT
  
  policy = quote_process.quote_policy
  if not policy:
    return QUOTE_STATUS_PAID
  
  return QUOTE_STATUS_DONE


def get_hereford_fee(deposit):
  return HEREFORD_FEES.get(deposit)