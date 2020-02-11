IMPORT_PROCESS_STATUS_PROCESSING = 'processing'
IMPORT_PROCESS_STATUS_DONE = 'done'
IMPORT_PROCESS_STATUS_ERROR = 'error'

IMPORT_PROCESS_STATUS_CHOICES = (
    (IMPORT_PROCESS_STATUS_DONE, 'Done'),
    (IMPORT_PROCESS_STATUS_PROCESSING, 'Processing'),
    (IMPORT_PROCESS_STATUS_ERROR, 'Error'),
)

# Old dataset
# NYC_API_MEDALLION_DRIVERS_DATASET_ID = "pm46-7vyh"
NYC_API_MEDALLION_DRIVERS_DATASET_ID = "jb3k-j3gp"
NYC_API_FOR_HIRE_VEHICLES_DATASET_ID = "k5sk-y8y9"
NYC_API_FHV_DRIVERS_DATASET_ID = "xjfq-wh2d"


NYC_XLSX_VEHICLES_INSURANCE_SOURCE = "https://www1.nyc.gov/assets/tlc/downloads/datasets/current_insurance.xlsx"
NYC_XLSX_VEHICLES_INSURANCE_HEADER = [
        "tlc_license_type",
        "tlc_license_number",
        "dmv_plate",
        "vin",
        "automobile_insurance_code",
        "automobile_insurance_name",
        "automobile_insurance_policy_number",
        "vehicle_owner_name",
        "affiliated_base_or_taxi_agent_or_fleet_license_number",
    ]
