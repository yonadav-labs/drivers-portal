import StepTLC from '@/apps/quote/views/steps/step-tlc.vue'
import StepConfirmTLC from '@/apps/quote/views/steps/step-confirm-tlc.vue'

export default [
    { path: '/', component: StepTLC, name:'quoteTlc'},
    { path: 'confirm-tlc/', component: StepConfirmTLC, name:'quoteTlcConfirm' }
]