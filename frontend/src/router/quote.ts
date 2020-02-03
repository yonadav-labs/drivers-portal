import StepTLC from '@/apps/quote/views/steps/step-tlc.vue'
import StepVIN from '@/apps/quote/views/steps/step-vin.vue'

export default [
  { path: '/', component: StepTLC, name:'quoteTlc'},
  { path: '/vin/', component: StepVIN, name: 'quoteVin' },
]