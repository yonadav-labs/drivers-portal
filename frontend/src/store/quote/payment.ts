import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';
import { QuoteProcessPayment } from '@/@types/quote';

import { APIProperty, APIState } from '@/store/api'
import { retrieveQuoteProcessPayment } from '@/store/quote/api'

@Module({ namespaced: true })
export default class QuotePaymentVuexModule extends VuexModule {
  apiQuoteProcessPayment: APIProperty<QuoteProcessPayment> = APIState.state<QuoteProcessPayment>()

  get quoteProcessPayment(): QuoteProcessPayment | undefined {
    return this.apiQuoteProcessPayment.data
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
}