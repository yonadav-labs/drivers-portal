import datetime

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


def get_quote_info(quote_process):
  date1 = 21 if quote_process.deposit > 15 else 15
  days = 20 if quote_process.deposit > 15 else 15
  date2 = quote_process.start_date + datetime.timedelta(days=days)
  nodp = (quote_process.start_date - datetime.date(2020, 3, 2)).days
  prp = quote_process.quote_amount * (363 - nodp) / 363
  deposit = quote_process.quote_amount * quote_process.deposit / 100
  omp = quote_process.quote_amount * (100 - quote_process.deposit) / 900
  fmp = prp - deposit - omp * 2
  hereford_fee = 30 if quote_process.deposit == 15 else 25 if quote_process.deposit == 20 else 20

  if quote_process.deposit == 100:
    deposit = prp
    omp = fmp = hereford_fee = 0

  resp = {
    'start_date': quote_process.start_date.strftime('%B %d %Y'),
    'annualized_premium': f'${quote_process.quote_amount}',
    'prorated_premium': f'${prp:,.2f}',
    'deposit_amount': f'${deposit:,.2f}',
    'monthly_payment1_date': f'{date2.strftime("%B %d")}',
    'monthly_payment1_amount': f'${fmp:,.2f}',
    'monthly_payment2_date': f'October {date1}',
    'monthly_payment2_amount': f'${omp:,.2f}',
    'monthly_payment3_date': f'November {date1}',
    'monthly_payment3_amount': f'${omp:,.2f}',
    'hereford_fee': f'${hereford_fee}',
  }

  return resp
