import { store } from '@/store/store'

import { QuoteProcessPayload, QuoteProcess } from '@/@types/quote';

import { OrderedQuoteRouteNames } from '@/router/quote'

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
    [OrderedQuoteRouteNames.TLC]: true,
    [OrderedQuoteRouteNames.VIN]: true,
    [OrderedQuoteRouteNames.QUESTION_LONG_TLC]: true,
    [OrderedQuoteRouteNames.QUESTION_LONG_DMV]: true,
    [OrderedQuoteRouteNames.QUESTION_DRIVER_POINTS]: true,
    [OrderedQuoteRouteNames.QUESTION_FAULT_ACCIDENTS]: true,
    [OrderedQuoteRouteNames.QUESTION_DEFENSIVE_CERTIFICATE]: true,
    [OrderedQuoteRouteNames.QUESTION_ACCIDENT_AVOIDANCE]: true,
    [OrderedQuoteRouteNames.EMAIL]: true,
  })
  
}