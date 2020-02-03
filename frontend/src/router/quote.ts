import StepTLC from '@/apps/quote/views/steps/step-tlc.vue'
import StepVIN from '@/apps/quote/views/steps/step-vin.vue'

export enum QuoteRouteNames {
  TLC = 'quoteTlc',
  VIN = 'quoteVin'
}

export default [
  { path: '/', component: StepTLC, name: QuoteRouteNames.TLC},
  { path: '/vin/', component: StepVIN, name: QuoteRouteNames.VIN },
]