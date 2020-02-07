import DashboardDocs from '@/apps/dashboard/views/docs.vue';

export enum DashboardRouteName {
  DOCS = 'dashboardDocs',
}

export default [
  { path: '/', component: DashboardDocs, name: DashboardRouteName.DOCS },
]

