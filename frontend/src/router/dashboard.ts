import DashboardDocs from '@/apps/dashboard/views/docs.vue';

export enum DashboardRouteName {}

export enum DashboardDocsRouteName {
  DOCS = 'dashboardDocs',
}

export class DashboardRouter {

  static isDocsRoute(name: string): boolean {
    return Object.values(DashboardDocsRouteName).includes(name as DashboardDocsRouteName)
  }
}

export default [
  { path: 'docs/', component: DashboardDocs, name: DashboardDocsRouteName.DOCS },
]

