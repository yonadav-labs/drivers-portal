import DashboardQuote from '@/apps/dashboard/views/quote.vue';
import DashboardQuoteUpload from '@/apps/dashboard/views/quote/upload.vue';
import DashboardQuotePayment from '@/apps/dashboard/views/quote/payment.vue';

import { QuoteStatus } from '@/@types/quote'

export enum DashboardRouteName {
  QUOTE = 'dashboardQuote',
}

export enum DashboardQuoteRouteName {
  UPLOAD = 'dashboardQuoteUpload',
  PAYMENT = 'dashboardQuotePayment'
}

export class DashboardRouter {

  static getRouteForQuoteStatus(status: QuoteStatus): { name: DashboardQuoteRouteName} {
    let route: DashboardQuoteRouteName;
  
    switch (status) {
      case 'payment':
      case 'paid':
        route = DashboardQuoteRouteName.PAYMENT
        break;

      case 'review':
      case 'docs':
      default:
        route = DashboardQuoteRouteName.UPLOAD
    }
    return { name: route }
  }

  static isDocsRoute(name: string): boolean {
    return Object.values(DashboardQuoteRouteName).includes(name as DashboardQuoteRouteName)
  }
}

const quoteRoutes = [
  { path: 'upload/', component: DashboardQuoteUpload, name: DashboardQuoteRouteName.UPLOAD },
  { path: 'payment/', component: DashboardQuotePayment, name: DashboardQuoteRouteName.PAYMENT }
]

export default [
  { path: 'quote/', component: DashboardQuote, name: DashboardRouteName.QUOTE, children: [
    ...quoteRoutes
  ] },

]
