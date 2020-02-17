import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';
import { PolicyList, PolicyDetail } from '@/@types/policy';

import { APIProperty, APIState } from '@/store/api'

import { listPolicies, retrievePolicy } from './api.ts'

@Module({ namespaced: true })
export default class UsersVuexModule extends VuexModule {
  apiPolicyList: APIProperty<PolicyList[]> = APIState.state<PolicyList[]>([]);
  apiPolicyById: { [id: string]: APIProperty<PolicyDetail> } = {}

  get policyList(): PolicyList[] {
    return this.apiPolicyList.data || []
  }

  get policyById(): (id: string) => PolicyDetail | undefined {
    return (id: string): PolicyDetail | undefined => (
      !!this.apiPolicyById[id] ? this.apiPolicyById[id].data:undefined
    )
  }

  @Mutation
  setApiPolicyListBlank(): void {
    this.apiPolicyList = APIState.state<PolicyList[]>([]);
  }

  @Mutation
  setApiPolicyListPending(): void {
    this.apiPolicyList = APIState.setPending(this.apiPolicyList);
  }

  @Mutation
  setApiPolicyList(payload: PolicyList[] | Error): void {
    this.apiPolicyList = APIState.update(this.apiPolicyList, payload)
  }

  @Mutation
  setApiPolicyByIdBlank(id: string): void {
    this.apiPolicyById = {
      ...this.apiPolicyById,
      [id]: APIState.state<PolicyDetail>()
    }
  }

  @Mutation
  setApiPolicyByIdPending(id: string): void {
    if (!!this.apiPolicyById[id]) {
      this.apiPolicyById = {
        ...this.apiPolicyById,
        [id]: APIState.setPending(this.apiPolicyById[id])
      }
    }
  }

  @Mutation
  setApiPolicyById({ id, payload }: {id: string, payload: PolicyDetail | Error}): void {
    if (!!this.apiPolicyById[id]) {
      this.apiPolicyById = {
        ...this.apiPolicyById,
        [id]: APIState.update(this.apiPolicyById[id], payload)
      }
    }
  }

  @Action
  async listPolicies(): Promise<void> {
    this.context.commit('setApiPolicyListBlank')
    this.context.commit('setApiPolicyListPending')

    try {
      const payload = await listPolicies();
      this.context.commit('setApiPolicyList', payload)
    } catch (e) {
      this.context.commit('setApiPolicyList', e)
    }
  }

  @Action
  async retrievePolicyById(id: string): Promise<void> {
    this.context.commit('setApiPolicyByIdBlank', id)
    this.context.commit('setApiPolicyByIdPending', id)

    try {
      const payload = await retrievePolicy(id);
      this.context.commit('setApiPolicyById', { id, payload})
    } catch (e) {
      this.context.commit('setApiPolicyById', { id, payload: e})
    }
  }
}