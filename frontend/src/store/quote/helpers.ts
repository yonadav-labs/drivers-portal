import { store } from '@/store/store'

import { QuoteProcessPayload, QuoteProcess } from '@/@types/quote';

import { OrderedQuoteRouteName } from '@/router/quote'

export function buildQuoteProcessPayload(): QuoteProcessPayload {
  return {
    ...store.getters['QuoteTlc/tlcLicenseName'],
    ...store.getters['QuoteVin/fhvInfo'],
    ...store.getters['QuoteVin/insuranceInfo'],
    ...store.getters['Quote/questionAnswers'],
    email: store.getters['Quote/quoteEmail']
  }
}

export function deconstructQuoteProcess(quoteProcess: QuoteProcess): void {
  const {
    tlc_number, tlc_name, vehicle_vin, vehicle_owner, license_plate, 
    base_name, base_number, vehicle_year, insurance_carrier_name,
    insurance_policy_number, tlc_license_years, dmv_license_years,
    driver_points_last_months, fault_accidents_last_months,
    defensive_driving_certificate, accident_avoidance_system,
    email
  } = quoteProcess
  store.commit('QuoteTlc/setTlcStepLicense', { tlc_number, tlc_name })
  store.commit('QuoteVin/setApiFHVInfo', { vehicle_vin, vehicle_owner, license_plate, base_name, base_number, vehicle_year })
  store.commit('QuoteVin/setApiInsuranceInfo', { insurance_carrier_name, insurance_policy_number })
  store.commit('Quote/setQuestionAnswers', {  
    tlc_license_years, dmv_license_years, driver_points_last_months, 
    fault_accidents_last_months, defensive_driving_certificate, 
    accident_avoidance_system 
  })
  store.commit('Quote/setQuoteEmail', email)

  store.commit('Quote/setMultipleStepsCompleted', {
    [OrderedQuoteRouteName.TLC]: true,
    [OrderedQuoteRouteName.VIN]: true,
    [OrderedQuoteRouteName.QUESTION_LONG_TLC]: true,
    [OrderedQuoteRouteName.QUESTION_LONG_DMV]: true,
    [OrderedQuoteRouteName.QUESTION_DRIVER_POINTS]: true,
    [OrderedQuoteRouteName.QUESTION_FAULT_ACCIDENTS]: true,
    [OrderedQuoteRouteName.QUESTION_DEFENSIVE_CERTIFICATE]: true,
    // [OrderedQuoteRouteName.QUESTION_ACCIDENT_AVOIDANCE]: true, DISABLED FOR NOW
    [OrderedQuoteRouteName.EMAIL]: true,
  })
  
}