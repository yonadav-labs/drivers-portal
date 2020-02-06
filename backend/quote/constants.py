TLC_LESS_ONE_YEAR = '<1'
TLC_ONE_THREE_YEARS = '1-3'
TLC_PLUS_THREE_YEARS = '3+'

TLC_YEAR_INTERVAL_CHOICES = (
    (TLC_LESS_ONE_YEAR, TLC_LESS_ONE_YEAR),
    (TLC_ONE_THREE_YEARS, TLC_ONE_THREE_YEARS),
    (TLC_PLUS_THREE_YEARS, TLC_PLUS_THREE_YEARS)
)

DMV_LESS_TWO_YEARS = '<2'
DMV_TWO_THREE_YEARS = '2-3'
DMV_PLUS_THREE_YEARS = '3+'

DMV_YEAR_INTERVAL_CHOICES = (
    (DMV_LESS_TWO_YEARS, DMV_LESS_TWO_YEARS),
    (DMV_TWO_THREE_YEARS, DMV_TWO_THREE_YEARS),
    (DMV_PLUS_THREE_YEARS, DMV_PLUS_THREE_YEARS)
)

POINTS_ZERO_SIX = '0-6'
POINTS_SEVEN_TEN = '7-10'
POINTS_MORE_TEN = '10+'

POINTS_CHOICES = (
    (POINTS_ZERO_SIX, POINTS_ZERO_SIX),
    (POINTS_SEVEN_TEN, POINTS_SEVEN_TEN),
    (POINTS_MORE_TEN, POINTS_MORE_TEN)
)

QUOTE_PROCESS_DEPOSIT_15 = 15
QUOTE_PROCESS_DEPOSIT_20 = 20
QUOTE_PROCESS_DEPOSIT_25 = 25

QUOTE_PROCESS_DEPOSIT_CHOICES = (
    (QUOTE_PROCESS_DEPOSIT_15, "15%"),
    (QUOTE_PROCESS_DEPOSIT_20, "20%"),
    (QUOTE_PROCESS_DEPOSIT_25, "25%"),
)

QUOTE_PROCESS_DEDUCTIBLE_750 = 750
QUOTE_PROCESS_DEDUCTIBLE_1000 = 1000
QUOTE_PROCESS_DEDUCTIBLE_1500 = 1500

QUOTE_PROCESS_DEDUCTIBLE_CHOICES = (
    (QUOTE_PROCESS_DEDUCTIBLE_750, "750"),
    (QUOTE_PROCESS_DEDUCTIBLE_1000, "1000"),
    (QUOTE_PROCESS_DEDUCTIBLE_1500, "1500")
)

FAULT_ACCIDENTS_ZERO = '0'
FAULT_ACCIDENTS_ONE = '1'
FAULT_ACCIDENTS_TWO = '2'
FAULT_ACCIDENTS_THREE = '3+'

FAULT_ACCIDENTS_CHOICES = (
    (FAULT_ACCIDENTS_ZERO, '0'),
    (FAULT_ACCIDENTS_ONE, '1'),
    (FAULT_ACCIDENTS_TWO, '2'),
    (FAULT_ACCIDENTS_THREE, '3+'),
)
