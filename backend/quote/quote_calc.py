from django.utils import timezone

from importer.constants import BASE_TYPE_BLACKCAR

from quote.constants import (
  VEHICLE_OWNER_DRIVER,
  VEHICLE_OWNER_NAMED,
  VEHICLE_OWNER_CORPORATE,
  FAULT_ACCIDENTS_ZERO,
  FAULT_ACCIDENTS_THREE,
  ACCIDENTS_72_ZERO,
  ACCIDENTS_72_FOUR,
  POINTS_ZERO_SIX,
  DMV_PLUS_THREE_YEARS,
  TLC_LESS_ONE_YEAR,
  POINTS_SEVEN_TEN,
  POINTS_MORE_TEN
)

BODILY = 'body_injury'
PROPERTY_DAMAGE = 'property_damage'
INJURY = 'personal_injury_protection'
ADDITIONAL = 'aditional_personal_injury_protection'


LIVERY_BASE_RATES = {
  VEHICLE_OWNER_DRIVER: {
    BODILY: 5199,
    PROPERTY_DAMAGE: 944,
    INJURY: 1474,
    ADDITIONAL: 439,
  },
  VEHICLE_OWNER_NAMED : {
    BODILY: 6560,
    PROPERTY_DAMAGE: 1192,
    INJURY: 1860,
    ADDITIONAL: 744,
  },
  VEHICLE_OWNER_CORPORATE : {
    BODILY: 7288,
    PROPERTY_DAMAGE: 1324,
    INJURY: 2066,
    ADDITIONAL: 827,
  },
}

BLACKCAR_BASE_RATES = {
  VEHICLE_OWNER_DRIVER: {
    BODILY: 2888,
    PROPERTY_DAMAGE: 703,
    INJURY: 1098,
    ADDITIONAL: 439,
  },
  VEHICLE_OWNER_NAMED : {
    BODILY: 3575,
    PROPERTY_DAMAGE: 946,
    INJURY: 1476,
    ADDITIONAL: 590,
  },
  VEHICLE_OWNER_CORPORATE : {
    BODILY: 3763,
    PROPERTY_DAMAGE: 996,
    INJURY: 1554,
    ADDITIONAL: 621,
  },
}


def get_accident_prevention(quote):
  return 0.9 if quote.defensive_driving_certificate else 1.0

def get_safe_driver(quote):
  condition = quote.fault_accidents_last_months == FAULT_ACCIDENTS_ZERO
  return 0.8 if condition else 1.0 

def get_longevity(quote):
  condition = False
  is_hereford = "hereford" in quote.insurance_carrier_name.lower()
  if is_hereford:
    try:
      value = int(quote.insurance_policy_number.split('-')[-1])
      condition = value >= 3
    except:
      condition = False
  return 0.97 if condition else 1.0

def get_workers_compensation(quote):
  condition = quote.base_type.base_type != BASE_TYPE_BLACKCAR
  return 0.95 if condition else 1.0

def get_loss_control(quote):
  condition = quote.base_type.loss_control_discount
  return 0.92 if condition else 1.0

def get_drive_cam(quote):
  condition = quote.dash_cam
  return 0.95 if condition else 1.0

def get_hybrid(quote):
  condition = quote.vehicle_is_hybrid
  return 0.95 if condition else 1.0

def extra_accidents(quote):
  condition = quote.accidents_72_months == ACCIDENTS_72_ZERO
  return 0.97 if condition else 1.0

def collision_avoidance(quote):
  condition = quote.accident_avoidance_system
  return 0.95 if condition else 1.0

def get_luxury(quote):
  condition = quote.vehicle_year >= 2016
  if condition:
    condition = quote.base_type.luxury_discount
  if condition:
    condition =  quote.fault_accidents_last_months == FAULT_ACCIDENTS_ZERO
  if condition:
    condition = quote.accidents_72_months != ACCIDENTS_72_FOUR
  if condition:
    condition = quote.driver_points_last_months == POINTS_ZERO_SIX
  return 0.92 if condition else 1.0

# Surcharges
def get_inexperienced(quote):
  condition = quote.dmv_license_years != DMV_PLUS_THREE_YEARS
  condition = condition or quote.tlc_license_years == TLC_LESS_ONE_YEAR
  return 1.15 if condition else 1.0

def get_dwi(quote):
  condition = quote.dwi_36_months
  return 1.15 if condition else 1.0

def get_pedestrian(quote):
  condition = quote.fault_accident_pedestrian
  return 1.10 if condition else 1.0

def get_speeding(quote):
  condition = quote.speeding_violation
  return 1.05 if condition else 1.0

def get_at_fault(quote):
  condition = quote.fault_accidents_last_months == FAULT_ACCIDENTS_THREE
  return 1.1 if condition else 1.0

def get_vehicle_old(quote):
  year = timezone.now().year
  condition = (year - quote.vehicle_year) > 11
  return 1.05 if condition else 1.0

def get_vehicle_weight(quote):
  condition = False
  return 1.01 if condition else 1.0

def get_mrv(quote):
  if quote.driver_points_last_months == POINTS_SEVEN_TEN:
    return 1.1
  elif quote.driver_points_last_months == POINTS_MORE_TEN:
    return 1.2
  else:
    return 1.0

DISCOUNTS = [
  get_accident_prevention,
  get_safe_driver,
  get_longevity,
  get_workers_compensation,
  get_loss_control,
  get_drive_cam,
  get_hybrid,
  extra_accidents,
  collision_avoidance,
  get_luxury,
]

SURCHARGES = [
  get_inexperienced,
  get_dwi,
  get_pedestrian,
  get_speeding,
  get_at_fault,
  get_vehicle_old,
  get_vehicle_weight,
  get_mrv
]


def get_quote_rate_variation(quote):
  rate = 1.0
  for discount_func in DISCOUNTS:
    rate *= discount_func(quote)
  
  for surcharge_func in SURCHARGES:
    rate *= surcharge_func(quote)
  return rate

def get_quote_variations(quote):
  rate_variation = get_quote_rate_variation(quote)
  base_rates = BLACKCAR_BASE_RATES if quote.base_type.base_type == BASE_TYPE_BLACKCAR \
    else LIVERY_BASE_RATES
  variations = base_rates[quote.vehicle_owner]

  total = 60.0
  final_rates = {
    'uninsured_motorist': 60.0
  }
  for key in variations.keys():
    amount = variations[key] * rate_variation
    total += amount
    final_rates[key] = amount
  
  final_rates['liability_total'] = total
  return final_rates
