from quote.constants import (
  QUOTE_PROCESS_DEDUCTIBLE_750, QUOTE_PROCESS_DEDUCTIBLE_1000, QUOTE_PROCESS_DEDUCTIBLE_1500,
    QUOTE_STATUS_CREATED, QUOTE_STATUS_DOCS, QUOTE_STATUS_REVIEW, QUOTE_STATUS_PAYMENT, 
    QUOTE_STATUS_PAID, QUOTE_STATUS_DONE, HEREFORD_FEES
)

def generate_variations(quote_process):
  # TODO: Implement real variations
  return {
    "liability_total":4581.0,
    "body_injury":2454.0,
    "property_damage":649.5,
    "personal_injury_protection":1012.5,
    "aditional_personal_injury_protection":405.0,
    "uninsured_motorist":60.0,
    "deductible": {
      QUOTE_PROCESS_DEDUCTIBLE_750: {
        "physical_total":432.25,
        "physical_comprehensive":261.25,
        "physical_collision":171.0
      },
      QUOTE_PROCESS_DEDUCTIBLE_1000: {
        "physical_total":378.58,
        "physical_comprehensive":237.5,
        "physical_collision":141.08
      },
      QUOTE_PROCESS_DEDUCTIBLE_1500: {
        "physical_total":320.62,
        "physical_comprehensive":213.75,
        "physical_collision":106.88
      }
    }
  }


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