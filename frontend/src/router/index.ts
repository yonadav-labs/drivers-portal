import VueRouter from 'vue-router'

import QuoteRoutes from './quote'

import QuoteMainView from '@/apps/quote/views/main.vue'

const routes = [
    { path: '/', component: QuoteMainView, children: [
        ...QuoteRoutes
    ]}
]

export const router = new VueRouter({
    mode: 'history',
    routes
})