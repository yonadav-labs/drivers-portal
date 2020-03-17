import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';
import { PolicyList, PolicyDetail } from '@/@types/policy';
import { StripeChargePayload, PlaidChargePayload } from '@/@types/payment';

import { APIProperty, APIState } from '@/store/api'

import { listPolicies, retrievePolicy, payPaymentPlaid, payPaymentStripe } from './api'

@Module({ namespaced: true })
export default class UsersVuexModule extends VuexModule {
  apiPolicyList: APIProperty<PolicyList[]> = APIState.state<PolicyList[]>([]);
  apiPolicyById: { [id: string]: APIProperty<PolicyDetail> } = {}
  apiStripeCharge: APIProperty<StripeChargePayload> = APIState.state<StripeChargePayload>();
  apiPlaidCharge: APIProperty<PlaidChargePayload> = APIState.state<PlaidChargePayload>();

  get policyList(): PolicyList[] {
    return this.apiPolicyList.data || []
  }

  get policyById(): (id: string) => PolicyDetail | undefined {
    return (id: string): PolicyDetail | undefined => (
      !!this.apiPolicyById[id] ? this.apiPolicyById[id].data:undefined
    )
  }

  get stripeError(): Error | undefined {
    return this.apiStripeCharge.error;
  }

  get plaidError(): Error | undefined {
    return this.apiPlaidCharge.error
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

  @Mutation
  setApiStripeChargeBlank(): void {
    this.apiStripeCharge = APIState.state<StripeChargePayload>();
  }

  @Mutation
  setApiStripeChargePending(): void {
    this.apiStripeCharge = APIState.setPending(this.apiStripeCharge)
  }

  @Mutation
  setApiStripeCharge(payload: StripeChargePayload | Error): void {
    this.apiStripeCharge = APIState.update(this.apiStripeCharge, payload);
  }

  @Mutation
  setApiPlaidChargeBlank(): void {
    this.apiPlaidCharge = APIState.state<PlaidChargePayload>();
  }

  @Mutation
  setApiPlaidChargePending(): void {
    this.apiPlaidCharge = APIState.setPending(this.apiPlaidCharge)
  }

  @Mutation
  setApiPlaidCharge(payload: PlaidChargePayload | Error): void {
    this.apiPlaidCharge = APIState.update(this.apiPlaidCharge, payload);
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

  @Action
  async payPaymentStripe({ id, charge }: {id: string, charge: StripeChargePayload}): Promise<void> {
    this.context.commit('setApiStripeChargeBlank');
    this.context.commit('setApiStripeChargePending');

    try {
      const response = await payPaymentStripe({id, charge});
      this.context.commit('setApiStripeCharge', response);
    } catch(e) {
      console.log(e)
      this.context.commit('setApiStripeCharge', e);
    }
  }

  @Action
  async payPaymentPlaid({ id, charge }: {id: string, charge: PlaidChargePayload}): Promise<void> {
    this.context.commit('setApiPlaidChargeBlank');
    this.context.commit('setApiPlaidChargePending');

    try {
      const response = await payPaymentPlaid({id, charge});
      this.context.commit('setApiPlaidCharge', response);
    } catch (e) {
      console.log(e)
      this.context.commit('setApiPlaidCharge', e);
    }
  }
}