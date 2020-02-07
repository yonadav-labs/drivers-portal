import VueRouter from 'vue-router'

import QuoteRoutes from './quote'
import DashboardRoutes from './dashboard'

import QuoteMainView from '@/apps/quote/views/main.vue'
import DashboardMainView from '@/apps/dashboard/views/main.vue'

const routes = [
    {
      path: '/dashboard', component: DashboardMainView, children: [
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