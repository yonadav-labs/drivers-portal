import VueRouter from 'vue-router'

import QuoteRoutes from './quote'
import DashboardRoutes from './dashboard'

import DepositPaymentView from '@/apps/quote/views/deposit-payment.vue'
import QuoteProcessMainView from '@/apps/quote/views/quote-process.vue'
import QuoteProcessReviewView from '@/apps/quote/views/quote-review.vue'
import DashboardMainView from '@/apps/dashboard/views/main.vue'

import LoginView from '@/views/login.vue'
import MagicLinkView from '@/views/magic-link.vue'
import ForgotPasswordView from '@/views/forgot-password.vue'
import ResetPasswordView from '@/views/reset-password.vue'

export enum RouteName {
  MAGIC_LINK = 'magic_link',
  DASHBOARD = 'dashboard',
  PAYMENT = 'payment',
  LOGIN = 'login',
  FORGOT = 'forgot',
  RESET = 'reset',
  REVIEW = 'review'
}

const routes = [
    { path: '/magic_link/:id/', component: MagicLinkView, name: RouteName.MAGIC_LINK, props: true },
    {
      path: '/dashboard/', component: DashboardMainView, name: RouteName.DASHBOARD, children: [
        ...DashboardRoutes
      ]
    },
    // TODO: Move this two to Quote
    {
      path: '/quote/review/', component: QuoteProcessReviewView, name: RouteName.REVIEW,
    },
    {
      path: '/quote/pay/', component: DepositPaymentView, name: RouteName.PAYMENT,
    }, 
    {
      path: '/login/', component: LoginView, name: RouteName.LOGIN
    },
    {
      path: '/forgot-password/', component: ForgotPasswordView, name: RouteName.FORGOT
    },
    {
      path: '/reset-password/:id/', component: ResetPasswordView, name: RouteName.RESET, props: true
    },
    { path: '/', component: QuoteProcessMainView, children: [
        ...QuoteRoutes
    ]},
]

export const router = new VueRouter({
    mode: 'history',
    routes
})