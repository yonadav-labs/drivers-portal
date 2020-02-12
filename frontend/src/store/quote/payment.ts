import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

import { QuoteProcessPayment } from '@/@types/quote';
import { StripeChargePayload, PlaidChargePayload } from '@/@types/payment';

import { APIProperty, APIState } from '@/store/api'
import { retrieveQuoteProcessPayment, payDepositStripe, payDepositPlaid } from '@/store/quote/api'

@Module({ namespaced: true })
export default class QuotePaymentVuexModule extends VuexModule {
  apiQuoteProcessPayment: APIProperty<QuoteProcessPayment> = APIState.state<QuoteProcessPayment>()
  apiStripeCharge: APIProperty<StripeChargePayload> = APIState.state<StripeChargePayload>();
  apiPlaidCharge: APIProperty<PlaidChargePayload> = APIState.state<PlaidChargePayload>();

  get quoteProcessPayment(): QuoteProcessPayment | undefined {
    return this.apiQuoteProcessPayment.data
  }

  get stripeChargeSuccess(): boolean {
    return this.apiStripeCharge.status === 'success';
  }

  get stripeError(): Error | undefined {
    return this.apiStripeCharge.error;
  }

  @Mutation
  setApiQuoteProcessPaymentBlank(): void {
    this.apiQuoteProcessPayment = APIState.state<QuoteProcessPayment>();
  }

  @Mutation
  setApiQuoteProcessPaymentPending(): void {
    this.apiQuoteProcessPayment = APIState.setPending(this.apiQuoteProcessPayment)
  }

  @Mutation
  setApiQuoteProcessPayment(payload: QuoteProcessPayment | Error): void {
    this.apiQuoteProcessPayment = APIState.update(this.apiQuoteProcessPayment, payload);
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
  async retrieveQuoteProcessPayment(): Promise<void> {
    this.context.commit('setApiQuoteProcessPaymentPending');

    try {
      const quoteProcessPayment = await retrieveQuoteProcessPayment();
      this.context.commit('setApiQuoteProcessPayment', quoteProcessPayment);
    } catch (e) {
      this.context.commit('setApiQuoteProcessPayment', e)
    }
  }

  @Action
  async payDepositStripe(charge: StripeChargePayload): Promise<void> {
    this.context.commit('setApiStripeChargeBlank');
    this.context.commit('setApiStripeChargePending');

    try {
      const response = await payDepositStripe(charge);
      this.context.commit('setApiStripeCharge', response);
    } catch(e) {
      console.log(e)
      this.context.commit('setApiStripeCharge', e);
    }
  }

  @Action
  async payDepositPlaid(charge: PlaidChargePayload): Promise<void> {
    this.context.commit('setApiPlaidChargeBlank');
    this.context.commit('setApiPlaidChargePending');

    try {
      const response = await payDepositPlaid(charge);
      this.context.commit('setApiPlaidCharge', response);
    } catch (e) {
      this.context.commit('setApiPlaidCharge', e);
    }
  }

  @Action
  resetPayments(): void {
    this.context.commit('setApiStripeChargeBlank');
    this.context.commit('setApiPlaidChargeBlank');
  }
}