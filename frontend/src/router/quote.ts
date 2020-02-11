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

export enum OrderedQuoteRouteName {
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
  [OrderedQuoteRouteName.TLC]: 0,
  [OrderedQuoteRouteName.VIN]: 1,
  [OrderedQuoteRouteName.QUESTION_LONG_TLC]: 2,
  [OrderedQuoteRouteName.QUESTION_LONG_DMV]: 3,
  [OrderedQuoteRouteName.QUESTION_DRIVER_POINTS]: 4,
  [OrderedQuoteRouteName.QUESTION_FAULT_ACCIDENTS]: 5,
  [OrderedQuoteRouteName.QUESTION_DEFENSIVE_CERTIFICATE]: 6,
  [OrderedQuoteRouteName.QUESTION_ACCIDENT_AVOIDANCE]: 7,
  [OrderedQuoteRouteName.EMAIL]: 8,
  [OrderedQuoteRouteName.QUOTE]: 9
}

const quoteRoutesByOrder = {
  [quoteRoutesOrder[OrderedQuoteRouteName.TLC]]: OrderedQuoteRouteName.TLC,
  [quoteRoutesOrder[OrderedQuoteRouteName.VIN]]: OrderedQuoteRouteName.VIN,
  [quoteRoutesOrder[OrderedQuoteRouteName.QUESTION_LONG_TLC]]: OrderedQuoteRouteName.QUESTION_LONG_TLC,
  [quoteRoutesOrder[OrderedQuoteRouteName.QUESTION_LONG_DMV]]: OrderedQuoteRouteName.QUESTION_LONG_DMV,
  [quoteRoutesOrder[OrderedQuoteRouteName.QUESTION_DRIVER_POINTS]]: OrderedQuoteRouteName.QUESTION_DRIVER_POINTS,
  [quoteRoutesOrder[OrderedQuoteRouteName.QUESTION_FAULT_ACCIDENTS]]: OrderedQuoteRouteName.QUESTION_FAULT_ACCIDENTS,
  [quoteRoutesOrder[OrderedQuoteRouteName.QUESTION_DEFENSIVE_CERTIFICATE]]: OrderedQuoteRouteName.QUESTION_DEFENSIVE_CERTIFICATE,
  [quoteRoutesOrder[OrderedQuoteRouteName.QUESTION_ACCIDENT_AVOIDANCE]]: OrderedQuoteRouteName.QUESTION_ACCIDENT_AVOIDANCE,
  [quoteRoutesOrder[OrderedQuoteRouteName.EMAIL]]: OrderedQuoteRouteName.EMAIL,
  [quoteRoutesOrder[OrderedQuoteRouteName.QUOTE]]: OrderedQuoteRouteName.QUOTE,
}

const quoteRoutesTitles = {
  [OrderedQuoteRouteName.TLC]: 'TLC License',
  [OrderedQuoteRouteName.VIN]: `Vehicle's VIN`,
  [OrderedQuoteRouteName.QUESTION_LONG_TLC]: 'Driver Questions(1 of 6)',
  [OrderedQuoteRouteName.QUESTION_LONG_DMV]: 'Driver Questions(2 of 6)',
  [OrderedQuoteRouteName.QUESTION_DRIVER_POINTS]: 'Driver Questions(3 of 6)',
  [OrderedQuoteRouteName.QUESTION_FAULT_ACCIDENTS]: 'Driver Questions(4 of 6)',
  [OrderedQuoteRouteName.QUESTION_DEFENSIVE_CERTIFICATE]: 'Driver Questions(5 of 6)',
  [OrderedQuoteRouteName.QUESTION_ACCIDENT_AVOIDANCE]: 'Driver Questions(6 of 6)',
  [OrderedQuoteRouteName.EMAIL]: 'Verify Email Address',
  [OrderedQuoteRouteName.QUOTE]: 'Quote'
}

export class QuoteProcessRouter {

  static hasPrevious(route: string): boolean {
    return quoteRoutesOrder[route as OrderedQuoteRouteName] !== 0
  }

  static previousRouteName(route: string): OrderedQuoteRouteName {
    const currentOrder = quoteRoutesOrder[route as OrderedQuoteRouteName];

    if (currentOrder === 0) {
      throw new Error('There is no previous route')
    }

    return quoteRoutesByOrder[currentOrder - 1];
  }

  static nextRouteName(route: string): OrderedQuoteRouteName {
    const currentOrder = quoteRoutesOrder[route as OrderedQuoteRouteName];

    if (currentOrder === (Object.keys(quoteRoutesByOrder).length - 1)) {
      throw new Error('There is no next route')
    }

    return quoteRoutesByOrder[currentOrder + 1];

  }

  static previousRoute(route: string): { name: OrderedQuoteRouteName } {
    return { name: QuoteProcessRouter.previousRouteName(route as OrderedQuoteRouteName) }
  }

  static nextRoute(route: string): { name: OrderedQuoteRouteName } {
    return { name: QuoteProcessRouter.nextRouteName(route) }
  }

  static isBefore(current: string, compareWith: string): boolean {
    return quoteRoutesOrder[current as OrderedQuoteRouteName] < quoteRoutesOrder[compareWith as OrderedQuoteRouteName]
  }

  static isLater(current: string, compareWith: string): boolean {
    return quoteRoutesOrder[compareWith as OrderedQuoteRouteName] < quoteRoutesOrder[current as OrderedQuoteRouteName]
  }

  static getRouteNameByOrder(order: number): OrderedQuoteRouteName | undefined {
    return quoteRoutesByOrder[order]
  }

  static getRouteByOrder(order: number): { name?: OrderedQuoteRouteName } {
    return { name: QuoteProcessRouter.getRouteNameByOrder(order) }
  }
  
  static getRouteTitle(route: string): string {
    return quoteRoutesTitles[route as OrderedQuoteRouteName];
  }
}

export default [
  { path: '', component: StepTLC, name: OrderedQuoteRouteName.TLC},
  { path: 'vin/', component: StepVIN, name: OrderedQuoteRouteName.VIN },
  { path: 'question-tlc/', component: StepQuestionLongTLC, name: OrderedQuoteRouteName.QUESTION_LONG_TLC },
  { path: 'question-dmv/', component: StepQuestionLongDMV, name: OrderedQuoteRouteName.QUESTION_LONG_DMV },
  { path: 'question-driver-points/', component: StepQuestionDriverPoints, name: OrderedQuoteRouteName.QUESTION_DRIVER_POINTS },
  { path: 'question-fault-accidents/', component: StepQuestionFaultAccidents, name: OrderedQuoteRouteName.QUESTION_FAULT_ACCIDENTS },
  { path: 'question-defensive-certificate/', component: StepQuestionDefensiveCertificate, name: OrderedQuoteRouteName.QUESTION_DEFENSIVE_CERTIFICATE },
  { path: 'question-accident-avoidance/', component: StepQuestionAccidentAvoidance, name: OrderedQuoteRouteName.QUESTION_ACCIDENT_AVOIDANCE },
  { path: 'email/', component: StepEmail, name: OrderedQuoteRouteName.EMAIL },
  { path: 'quote/:quoteId/', component: StepQuote, name: OrderedQuoteRouteName.QUOTE, props: true },
  { path: 'error/', component: StepQuoteSoftFallout, name: ExtraQuoteRouteNames.SOFT_FALLOUT }
]