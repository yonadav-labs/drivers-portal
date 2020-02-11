import DashboardQuote from '@/apps/dashboard/views/quote.vue';
import DashboardUpload from '@/apps/dashboard/views/quote/upload.vue';

import { QuoteStatus } from '@/@types/quote'

export enum DashboardRouteName {
  QUOTE = 'dashboardQuote'
}

export enum DashboardQuoteRouteName {
  UPLOAD = 'dashboardUpload',
}

export class DashboardRouter {

  static getRouteForQuoteStatus(status: QuoteStatus): { name: DashboardQuoteRouteName} {
    let route: DashboardQuoteRouteName;
  
    switch (status) {
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
  { path: 'upload/', component: DashboardUpload, name: DashboardQuoteRouteName.UPLOAD },
]

export default [
  { path: 'quote/', component: DashboardQuote, name: DashboardRouteName.QUOTE, children: [
    ...quoteRoutes
  ] },

]

