import DashboardDocs from '@/apps/dashboard/views/docs.vue';

export enum DashboardRouteName {
  DOCS = 'dashboardDocs',
}

export default [
  { path: 'docs/', component: DashboardDocs, name: DashboardRouteName.DOCS },
]

