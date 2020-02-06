import StepTLC from '@/apps/quote/views/steps/step-tlc.vue'
import StepVIN from '@/apps/quote/views/steps/step-vin.vue'
import StepQuestionLongTLC from '@/apps/quote/views/steps/step-question-long-tlc.vue'
import StepQuestionLongDMV from '@/apps/quote/views/steps/step-question-long-dmv.vue'
import StepQuestionDriverPoints from '@/apps/quote/views/steps/step-question-driver-points.vue'
import StepQuestionFaultAccidents from '@/apps/quote/views/steps/step-question-fault-accidents.vue'
import StepQuestionDefensiveCertificate from '@/apps/quote/views/steps/step-question-defensive-certificate.vue'
import StepQuestionAccidentAvoidance from '@/apps/quote/views/steps/step-question-accident-avoidance.vue'
import StepEmail from '@/apps/quote/views/steps/step-email.vue'
import StepQuote from '@/apps/quote/views/steps/step-quote.vue'
import StepQuoteSoftFallout from '@/apps/quote/views/steps/step-quote-soft-fallout.vue'

export enum OrderedQuoteRouteNames {
  TLC = 'quoteTlc',
  VIN = 'quoteVin',
  QUESTION_LONG_TLC = 'quoteQuestionLongTLC',
  QUESTION_LONG_DMV = 'quoteQuestionLongDMV',
  QUESTION_DRIVER_POINTS = 'quoteQuestionDriverPoints',
  QUESTION_FAULT_ACCIDENTS = 'quoteQuestionFaultAccidents',
  QUESTION_DEFENSIVE_CERTIFICATE = 'quoteQuestionDefensiveCertificate',
  QUESTION_ACCIDENT_AVOIDANCE = 'quoteQuestionAccidentAvoidance',
  EMAIL = 'quoteEmail',
  QUOTE = 'quoteQuote'
}

export enum ExtraQuoteRouteNames {
  SOFT_FALLOUT = 'quoteSoftFallout',
}

const quoteRoutesOrder = {
  [OrderedQuoteRouteNames.TLC]: 0,
  [OrderedQuoteRouteNames.VIN]: 1,
  [OrderedQuoteRouteNames.QUESTION_LONG_TLC]: 2,
  [OrderedQuoteRouteNames.QUESTION_LONG_DMV]: 3,
  [OrderedQuoteRouteNames.QUESTION_DRIVER_POINTS]: 4,
  [OrderedQuoteRouteNames.QUESTION_FAULT_ACCIDENTS]: 5,
  [OrderedQuoteRouteNames.QUESTION_DEFENSIVE_CERTIFICATE]: 6,
  [OrderedQuoteRouteNames.QUESTION_ACCIDENT_AVOIDANCE]: 7,
  [OrderedQuoteRouteNames.EMAIL]: 8,
  [OrderedQuoteRouteNames.QUOTE]: 9
}

const quoteRoutesByOrder = {
  [quoteRoutesOrder[OrderedQuoteRouteNames.TLC]]: OrderedQuoteRouteNames.TLC,
  [quoteRoutesOrder[OrderedQuoteRouteNames.VIN]]: OrderedQuoteRouteNames.VIN,
  [quoteRoutesOrder[OrderedQuoteRouteNames.QUESTION_LONG_TLC]]: OrderedQuoteRouteNames.QUESTION_LONG_TLC,
  [quoteRoutesOrder[OrderedQuoteRouteNames.QUESTION_LONG_DMV]]: OrderedQuoteRouteNames.QUESTION_LONG_DMV,
  [quoteRoutesOrder[OrderedQuoteRouteNames.QUESTION_DRIVER_POINTS]]: OrderedQuoteRouteNames.QUESTION_DRIVER_POINTS,
  [quoteRoutesOrder[OrderedQuoteRouteNames.QUESTION_FAULT_ACCIDENTS]]: OrderedQuoteRouteNames.QUESTION_FAULT_ACCIDENTS,
  [quoteRoutesOrder[OrderedQuoteRouteNames.QUESTION_DEFENSIVE_CERTIFICATE]]: OrderedQuoteRouteNames.QUESTION_DEFENSIVE_CERTIFICATE,
  [quoteRoutesOrder[OrderedQuoteRouteNames.QUESTION_ACCIDENT_AVOIDANCE]]: OrderedQuoteRouteNames.QUESTION_ACCIDENT_AVOIDANCE,
  [quoteRoutesOrder[OrderedQuoteRouteNames.EMAIL]]: OrderedQuoteRouteNames.EMAIL,
  [quoteRoutesOrder[OrderedQuoteRouteNames.QUOTE]]: OrderedQuoteRouteNames.QUOTE,
}

const quoteRoutesTitles = {
  [OrderedQuoteRouteNames.TLC]: 'TLC License',
  [OrderedQuoteRouteNames.VIN]: `Vehicle's VIN`,
  [OrderedQuoteRouteNames.QUESTION_LONG_TLC]: 'Driver Questions(1 of 6)',
  [OrderedQuoteRouteNames.QUESTION_LONG_DMV]: 'Driver Questions(2 of 6)',
  [OrderedQuoteRouteNames.QUESTION_DRIVER_POINTS]: 'Driver Questions(3 of 6)',
  [OrderedQuoteRouteNames.QUESTION_FAULT_ACCIDENTS]: 'Driver Questions(4 of 6)',
  [OrderedQuoteRouteNames.QUESTION_DEFENSIVE_CERTIFICATE]: 'Driver Questions(5 of 6)',
  [OrderedQuoteRouteNames.QUESTION_ACCIDENT_AVOIDANCE]: 'Driver Questions(6 of 6)',
  [OrderedQuoteRouteNames.EMAIL]: 'Verify Email Address',
  [OrderedQuoteRouteNames.QUOTE]: 'Quote'
}

export class QuoteProcessRouter {

  static hasPrevious(route: string): boolean {
    return quoteRoutesOrder[route as OrderedQuoteRouteNames] !== 0
  }

  static previousRouteName(route: string): OrderedQuoteRouteNames {
    const currentOrder = quoteRoutesOrder[route as OrderedQuoteRouteNames];

    if (currentOrder === 0) {
      throw new Error('There is no previous route')
    }

    return quoteRoutesByOrder[currentOrder - 1];
  }

  static nextRouteName(route: string): OrderedQuoteRouteNames {
    const currentOrder = quoteRoutesOrder[route as OrderedQuoteRouteNames];

    if (currentOrder === (Object.keys(quoteRoutesByOrder).length - 1)) {
      throw new Error('There is no next route')
    }

    return quoteRoutesByOrder[currentOrder + 1];

  }

  static previousRoute(route: string): { name: OrderedQuoteRouteNames } {
    return { name: QuoteProcessRouter.previousRouteName(route as OrderedQuoteRouteNames) }
  }

  static nextRoute(route: string): { name: OrderedQuoteRouteNames } {
    return { name: QuoteProcessRouter.nextRouteName(route) }
  }

  static isBefore(current: string, compareWith: string): boolean {
    return quoteRoutesOrder[current as OrderedQuoteRouteNames] < quoteRoutesOrder[compareWith as OrderedQuoteRouteNames]
  }

  static isLater(current: string, compareWith: string): boolean {
    return quoteRoutesOrder[compareWith as OrderedQuoteRouteNames] < quoteRoutesOrder[current as OrderedQuoteRouteNames]
  }

  static getRouteNameByOrder(order: number): OrderedQuoteRouteNames | undefined {
    return quoteRoutesByOrder[order]
  }

  static getRouteByOrder(order: number): { name?: OrderedQuoteRouteNames } {
    return { name: QuoteProcessRouter.getRouteNameByOrder(order) }
  }
  
  static getRouteTitle(route: string): string {
    return quoteRoutesTitles[route as OrderedQuoteRouteNames];
  }
}

export default [
  { path: '/', component: StepTLC, name: OrderedQuoteRouteNames.TLC},
  { path: '/vin/', component: StepVIN, name: OrderedQuoteRouteNames.VIN },
  { path: '/question-tlc/', component: StepQuestionLongTLC, name: OrderedQuoteRouteNames.QUESTION_LONG_TLC },
  { path: '/question-dmv/', component: StepQuestionLongDMV, name: OrderedQuoteRouteNames.QUESTION_LONG_DMV },
  { path: '/question-driver-points/', component: StepQuestionDriverPoints, name: OrderedQuoteRouteNames.QUESTION_DRIVER_POINTS },
  { path: '/question-fault-accidents/', component: StepQuestionFaultAccidents, name: OrderedQuoteRouteNames.QUESTION_FAULT_ACCIDENTS },
  { path: '/question-defensive-certificate/', component: StepQuestionDefensiveCertificate, name: OrderedQuoteRouteNames.QUESTION_DEFENSIVE_CERTIFICATE },
  { path: '/question-accident-avoidance/', component: StepQuestionAccidentAvoidance, name: OrderedQuoteRouteNames.QUESTION_ACCIDENT_AVOIDANCE },
  { path: '/email/', component: StepEmail, name: OrderedQuoteRouteNames.EMAIL },
  { path: '/quote/:quoteId/', component: StepQuote, name: OrderedQuoteRouteNames.QUOTE, props: true },
  { path: '/error/', component: StepQuoteSoftFallout, name: ExtraQuoteRouteNames.SOFT_FALLOUT }
]