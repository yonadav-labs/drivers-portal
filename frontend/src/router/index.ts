import VueRouter from 'vue-router'

import QuoteRoutes from './quote'
import DashboardRoutes from './dashboard'

import QuoteMainView from '@/apps/quote/views/main.vue'
import DashboardMainView from '@/apps/dashboard/views/main.vue'

import MagicLinkView from '@/views/magic-link.vue'

export enum RouteName {
  MAGIC_LINK = 'magic_link',
  DASHBOARD = 'dashboard'
}

const routes = [
    { path: '/magic_link/:id/', component: MagicLinkView, name: RouteName.MAGIC_LINK, props: true },
    {
      path: '/dashboard/', component: DashboardMainView, name: RouteName.DASHBOARD, children: [
        ...DashboardRoutes
      ]
    },
    { path: '/', component: QuoteMainView, children: [
        ...QuoteRoutes
    ]},
]

export const router = new VueRouter({
    mode: 'history',
    routes
})