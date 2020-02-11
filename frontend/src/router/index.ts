import VueRouter from 'vue-router'

import QuoteRoutes from './quote'
import DashboardRoutes from './dashboard'

import QuoteProcessMainView from '@/apps/quote/views/quote-process.vue'
import QuoteProcessPaymentView from '@/apps/quote/views/payment.vue'
import DashboardMainView from '@/apps/dashboard/views/main.vue'

import LoginView from '@/views/login.vue'
import MagicLinkView from '@/views/magic-link.vue'

export enum RouteName {
  MAGIC_LINK = 'magic_link',
  DASHBOARD = 'dashboard',
  PAYMENT = 'payment',
  LOGIN = 'login',
}

const routes = [
    { path: '/magic_link/:id/', component: MagicLinkView, name: RouteName.MAGIC_LINK, props: true },
    {
      path: '/dashboard/', component: DashboardMainView, name: RouteName.DASHBOARD, children: [
        ...DashboardRoutes
      ]
    },
    {
      path: '/payment/:quoteId/', component: QuoteProcessPaymentView, name: RouteName.PAYMENT, props: true
    },
    {
      path: '/login/', component: LoginView, name: RouteName.LOGIN
    },
    { path: '/', component: QuoteProcessMainView, children: [
        ...QuoteRoutes
    ]},
]

export const router = new VueRouter({
    mode: 'history',
    routes
})