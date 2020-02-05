import StepTLC from '@/apps/quote/views/steps/step-tlc.vue'
import StepVIN from '@/apps/quote/views/steps/step-vin.vue'
import StepQuestionLongTLC from '@/apps/quote/views/steps/step-question-long-tlc.vue'
import StepQuestionLongDMV from '@/apps/quote/views/steps/step-question-long-dmv.vue'
import StepQuestionDriverPoints from '@/apps/quote/views/steps/step-question-driver-points.vue'
import StepQuestionFaultAccidents from '@/apps/quote/views/steps/step-question-fault-accidents.vue'
import StepQuestionDefensiveCertificate from '@/apps/quote/views/steps/step-question-defensive-certificate.vue'
import StepQuestionAccidentAvoidance from '@/apps/quote/views/steps/step-question-accident-avoidance.vue'
import StepEmail from '@/apps/quote/views/steps/step-email.vue'

export enum QuoteRouteNames {
  TLC = 'quoteTlc',
  VIN = 'quoteVin',
  QUESTION_LONG_TLC = 'quoteQuestionLongTLC',
  QUESTION_LONG_DMV = 'quoteQuestionLongDMV',
  QUESTION_DRIVER_POINTS = 'quoteQuestionDriverPoints',
  QUESTION_FAULT_ACCIDENTS = 'quoteQuestionFaultAccidents',
  QUESTION_DEFENSIVE_CERTIFICATE = 'quoteQuestionDefensiveCertificate',
  QUESTION_ACCIDENT_AVOIDANCE = 'quoteQuestionAccidentAvoidance',
  EMAIL = 'quoteEmail'
}

const quoteRoutesOrder = {
  [QuoteRouteNames.TLC]: 0,
  [QuoteRouteNames.VIN]: 1,
  [QuoteRouteNames.QUESTION_LONG_TLC]: 2,
  [QuoteRouteNames.QUESTION_LONG_DMV]: 3,
  [QuoteRouteNames.QUESTION_DRIVER_POINTS]: 4,
  [QuoteRouteNames.QUESTION_FAULT_ACCIDENTS]: 5,
  [QuoteRouteNames.QUESTION_DEFENSIVE_CERTIFICATE]: 6,
  [QuoteRouteNames.QUESTION_ACCIDENT_AVOIDANCE]: 7,
  [QuoteRouteNames.EMAIL]: 8,
}

const quoteRoutesByOrder = {
  [quoteRoutesOrder[QuoteRouteNames.TLC]]: QuoteRouteNames.TLC,
  [quoteRoutesOrder[QuoteRouteNames.VIN]]: QuoteRouteNames.VIN,
  [quoteRoutesOrder[QuoteRouteNames.QUESTION_LONG_TLC]]: QuoteRouteNames.QUESTION_LONG_TLC,
  [quoteRoutesOrder[QuoteRouteNames.QUESTION_LONG_DMV]]: QuoteRouteNames.QUESTION_LONG_DMV,
  [quoteRoutesOrder[QuoteRouteNames.QUESTION_DRIVER_POINTS]]: QuoteRouteNames.QUESTION_DRIVER_POINTS,
  [quoteRoutesOrder[QuoteRouteNames.QUESTION_FAULT_ACCIDENTS]]: QuoteRouteNames.QUESTION_FAULT_ACCIDENTS,
  [quoteRoutesOrder[QuoteRouteNames.QUESTION_DEFENSIVE_CERTIFICATE]]: QuoteRouteNames.QUESTION_DEFENSIVE_CERTIFICATE,
  [quoteRoutesOrder[QuoteRouteNames.QUESTION_ACCIDENT_AVOIDANCE]]: QuoteRouteNames.QUESTION_ACCIDENT_AVOIDANCE,
  [quoteRoutesOrder[QuoteRouteNames.EMAIL]]: QuoteRouteNames.EMAIL,
}

export class QuoteProcessRouter {

  static previousRouteName(route: QuoteRouteNames): QuoteRouteNames {
    const currentOrder = quoteRoutesOrder[route];

    if (currentOrder === 0) {
      throw new Error('There is no previous route')
    }

    return quoteRoutesByOrder[currentOrder - 1];
  }

  static nextRouteName(route: QuoteRouteNames): QuoteRouteNames {
    const currentOrder = quoteRoutesOrder[route];

    if (currentOrder === (Object.keys(quoteRoutesByOrder).length - 1)) {
      throw new Error('There is no next route')
    }

    return quoteRoutesByOrder[currentOrder + 1];

  }

  static previousRoute(route: QuoteRouteNames): { name: QuoteRouteNames } {
    return { name: QuoteProcessRouter.previousRouteName(route) }
  }

  static nextRoute(route: QuoteRouteNames): { name: QuoteRouteNames } {
    return { name: QuoteProcessRouter.nextRouteName(route) }
  }

  static isBefore(current: QuoteRouteNames, compareWith: QuoteRouteNames): boolean {
    return quoteRoutesOrder[current] < quoteRoutesOrder[compareWith]
  }

  static isLater(current: QuoteRouteNames, compareWith: QuoteRouteNames): boolean {
    return quoteRoutesOrder[compareWith] < quoteRoutesOrder[current]
  }
}

export default [
  { path: '/', component: StepTLC, name: QuoteRouteNames.TLC},
  { path: '/vin/', component: StepVIN, name: QuoteRouteNames.VIN },
  { path: '/question-tlc/', component: StepQuestionLongTLC, name: QuoteRouteNames.QUESTION_LONG_TLC },
  { path: '/question-dmv/', component: StepQuestionLongDMV, name: QuoteRouteNames.QUESTION_LONG_DMV },
  { path: '/question-driver-points/', component: StepQuestionDriverPoints, name: QuoteRouteNames.QUESTION_DRIVER_POINTS },
  { path: '/question-fault-accidents/', component: StepQuestionFaultAccidents, name: QuoteRouteNames.QUESTION_FAULT_ACCIDENTS },
  { path: '/question-defensive-certificate/', component: StepQuestionDefensiveCertificate, name: QuoteRouteNames.QUESTION_DEFENSIVE_CERTIFICATE },
  { path: '/question-accident-avoidance/', component: StepQuestionAccidentAvoidance, name: QuoteRouteNames.QUESTION_ACCIDENT_AVOIDANCE },
  { path: '/email/', component: StepEmail, name: QuoteRouteNames.EMAIL }
]