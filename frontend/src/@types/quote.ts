export interface TLCStepLicenseName {
    license_number: string,
    name: string
}

export interface VINStepFHVInfo {
  vehicle_vin: string,
  vehicle_owner: string,
  license_plate: string,
  base_name: string,
  base_number: string,
  vehicle_year: number,
}

export interface VINStepInsuranceInfo {
  insurance_carrier_name: string,
  insurance_policy_number: string,
}

export interface QuestionsStep {
  tlc_license_years?: string,
  dmv_license_years?: string,
  driver_points_last_months?: string,
  fault_accidents_last_months?: string,
  defensive_driving_certificate?: boolean,
  accident_avoidance_system?: boolean
}