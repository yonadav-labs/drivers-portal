from quote.constants import (
  QUOTE_PROCESS_DEDUCTIBLE_750, QUOTE_PROCESS_DEDUCTIBLE_1000, QUOTE_PROCESS_DEDUCTIBLE_1500
)

def calc_quote_amount(quote_process):
  # TODO: Implement real quote calcs
  return 1000


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