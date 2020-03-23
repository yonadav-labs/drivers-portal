export interface TLCStepLicenseName {
    tlc_number: string,
    tlc_name: string
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

interface MandatoryQuestionStep {
  tlc_license_years?: string,
  dmv_license_years?: string,
  driver_points_last_months?: string,
  fault_accidents_last_months?: string,
  defensive_driving_certificate?: boolean,
  accident_avoidance_system?: boolean,
  dash_cam?: boolean,
  vehicle_is_hybrid?: boolean,
  dwi_36_months?: boolean,
  fault_accident_pedestrian?: boolean,
  speeding_violation?: boolean,
  vehicle_owner?: string  
}

export interface QuestionsStep extends MandatoryQuestionStep {
  accidents_72_months?: string
}


export interface QuoteProcessOptions {
  deposit?: number,
  deductible?: number,
  start_date?: string,
  quote_amount?: number
}

export interface QuoteProcessOptionsPayload {
  deposit: number,
  deductible?: number,
  start_date: string,
}

export interface QuoteProcessPayload extends TLCStepLicenseName, VINStepFHVInfo, VINStepInsuranceInfo, Required<MandatoryQuestionStep> {
  email: string,
  accidents_72_months?: string
}

export type QuoteStatus = 'created' | 'docs' | 'review' | 'payment' | 'paid' | 'done'

export interface QuoteProcess extends QuoteProcessPayload, QuoteProcessOptions  {
  id: string,
  status: QuoteStatus,
  is_hereford: boolean
}

export interface QuoteSoftFallout {
  name: string,
  email: string,
  phone_number?: string
}

export interface QuoteProcessVariationPhysical {
  physical_total: number,
  physical_comprehensive: number,
  physical_collision: number,
}


interface BaseQuoteProcessVariations {
  liability_total: number
  body_injury: number
  property_damage: number
  personal_injury_protection: number
  aditional_personal_injury_protection: number
  uninsured_motorist: number
}

export interface QuoteProcessCalcVariations extends BaseQuoteProcessVariations{ 
  deductible: QuoteProcessVariationPhysical[]
}

export interface QuoteProcessDocumentsAccidentReport {
  id: string,
  accident_report?: string
}

export interface QuoteProcessDocuments {
  id: string,
  dmv_license_front_side: string,
  dmv_license_back_side: string,
  tlc_license_front_sid: string,
  tlc_license_back_side: string,
  proof_of_address: string,
  base_letter: string,
  defensive_driving_certificate: string,
  is_submitted_for_review: boolean,
  is_broker_of_record_signed: boolean,
  requires_broker_of_record: boolean
  accident_reports: QuoteProcessDocumentsAccidentReport[],
  [key: string]: any
}

export interface QuoteProcessPayment {
  official_hereford_quote: number,
  liability_amount?: number,
  physical_amount?: number,
  payment_date: string,
  deposit: number,
  monthly_payment: number,
  hereford_fee: number,
  stripe_fee: number,
  plaid_fee: number,
  deposit_payment_amount: number,
  deposit_percentage: number,
  has_third_party_deposit: boolean,
  third_party_name: string,
  third_party_amount: number,
}
