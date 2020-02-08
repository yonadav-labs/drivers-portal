import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

import { 
  QuestionsStep, QuoteProcess, QuoteSoftFallout,
  QuoteProcessCalcVariations
} from '@/@types/quote';

import { APIProperty, APIState } from '@/store/api'
import {
  createQuoteProcess, retrieveQuoteProcessById, updateQuoteProcess,
  createQuoteSoftFallout, retrieveCalcQuoteProcessVariations
} from '@/store/quote/api'

import { checkEmailExists as apiCheckEmailExists } from '@/store/users/api'

import { OrderedQuoteRouteNames } from '@/router/quote'

import { buildQuoteProcessPayload, deconstructQuoteProcess } from './helpers'

@Module({ namespaced: true })
export default class QuoteMainVuexModule extends VuexModule {
  apiQuoteProcess: APIProperty<QuoteProcess> = APIState.state<QuoteProcess>();
  apiQuoteSoftFallout: APIProperty<QuoteSoftFallout> = APIState.state<QuoteSoftFallout>();
  apiQuoteProcessCalcVariations: APIProperty<QuoteProcessCalcVariations> = APIState.state<QuoteProcessCalcVariations>();
  internalEmailExist = false;
  internalQuestionAnswers: QuestionsStep = {}
  internalQuoteEmail = '';
  stepsCompleted = {
    [OrderedQuoteRouteNames.TLC]: false,
    [OrderedQuoteRouteNames.VIN]: false,
    [OrderedQuoteRouteNames.QUESTION_LONG_TLC]: false,
    [OrderedQuoteRouteNames.QUESTION_LONG_DMV]: false,
    [OrderedQuoteRouteNames.QUESTION_DRIVER_POINTS]: false,
    [OrderedQuoteRouteNames.QUESTION_FAULT_ACCIDENTS]: false,
    [OrderedQuoteRouteNames.QUESTION_DEFENSIVE_CERTIFICATE]: false,
    [OrderedQuoteRouteNames.QUESTION_ACCIDENT_AVOIDANCE]: false,
    [OrderedQuoteRouteNames.EMAIL]: false,
    [OrderedQuoteRouteNames.QUOTE]: false
  }

  get emailExists(): boolean {
    return this.internalEmailExist
  }

  get questionAnswers(): QuestionsStep {
    return this.internalQuestionAnswers
  }

  get quoteEmail(): string {
    return this.internalQuoteEmail;
  }

  get quoteProcess(): QuoteProcess | undefined {
    return this.apiQuoteProcess.data;
  }

  get quoteProcessId(): string | undefined {
    return (this.apiQuoteProcess.data || {}).id
  }

  get quoteProcessCalcVariations(): QuoteProcessCalcVariations | undefined {
    return this.apiQuoteProcessCalcVariations.data
  }

  get stepCompletedByName(): (name: OrderedQuoteRouteNames) => boolean {
    return (name: OrderedQuoteRouteNames) => this.stepsCompleted[name];
  }

  @Mutation
  setEmailExists(value: boolean): void {
    this.internalEmailExist = value;
  }

  @Mutation
  setMultipleStepsCompleted(payload: { step: OrderedQuoteRouteNames, value: boolean }): void {
    this.stepsCompleted = {
      ...this.stepsCompleted,
      ...payload
    }
  }

  @Mutation
  setQuoteEmail(value: string): void {
    this.internalQuoteEmail = value;
  }

  @Mutation
  setQuestionAnswers(payload: QuestionsStep): void {
    this.internalQuestionAnswers = {
      ...payload
    }
  }

  @Mutation
  setQuoteProcess(payload: QuoteProcess): void {
    this.apiQuoteProcess = APIState.update(this.apiQuoteProcess, payload)
  }

  @Mutation
  setQuoteProcessBlank(): void {
    this.apiQuoteProcess = APIState.state<QuoteProcess>();
  }

  @Mutation
  setQuoteProcessPending(): void {
    this.apiQuoteProcess = APIState.setPending(this.apiQuoteProcess)
  }

  @Mutation
  setQuoteProcessCalcVariationsBlank(): void {
    this.apiQuoteProcessCalcVariations = APIState.state<QuoteProcessCalcVariations>();
  }
  @Mutation
  setQuoteProcessCalcVariationsPending(): void {
    this.apiQuoteProcessCalcVariations = APIState.setPending(this.apiQuoteProcessCalcVariations)
  }

  @Mutation
  setQuoteProcessCalcVariations(payload: QuoteProcessCalcVariations | Error): void {
    this.apiQuoteProcessCalcVariations = APIState.update(this.apiQuoteProcessCalcVariations, payload);
  }

  @Mutation
  setQuoteSoftFallout(payload: QuoteSoftFallout): void {
    this.apiQuoteSoftFallout = APIState.update(this.apiQuoteSoftFallout, payload)
  }

  @Mutation
  setQuoteSoftFalloutBlank(): void {
    this.apiQuoteSoftFallout = APIState.state<QuoteSoftFallout>();
  }

  @Mutation
  setQuoteSoftFalloutPending(): void {
    this.apiQuoteSoftFallout = APIState.setPending(this.apiQuoteSoftFallout)
  }

  @Mutation
  setStepCompleted(payload: { step: OrderedQuoteRouteNames, value: boolean }): void {
    const { step, value } = payload;
    this.stepsCompleted = {
      ...this.stepsCompleted,
      [step]: value
    }
  }

  @Action
  async createOrUpdateQuoteProcess(): Promise<void> {
    this.context.commit('setQuoteProcessPending')
    const data = buildQuoteProcessPayload();
    try {
      const existing = await updateQuoteProcess(data.email, data)
      this.context.commit('setQuoteProcess', existing)
    } catch (updateError) {
      try {
        const created = await createQuoteProcess(data)
        this.context.commit('setQuoteProcess', created)
      } catch (createError) {
        this.context.commit('setQuoteProcess', createError)
        console.error(createError)
      }
    }
  }

  @Action
  async checkEmailExists(email: string): Promise<void> {
    this.context.commit('setEmailExists', false);
    try {
      await apiCheckEmailExists(email);
      this.context.commit('setEmailExists', true);
    } catch (e) {
      this.context.commit('setEmailExists', false);
    }
  }

  @Action
  async createQuoteSoftFallout(payload: QuoteSoftFallout): Promise<void> {
    this.context.commit('setQuoteSoftFalloutPending');
    try {
      const quoteFallout = await createQuoteSoftFallout(payload);
      this.context.commit('setQuoteSoftFallout', quoteFallout)
    } catch (e) {
      this.context.commit('setQuoteSoftFallout', e)
    }
  }

  @Action
  resetEmailExists(): void {
    this.context.commit('setEmailExists', false);
  }

  @Action
  async retrieveQuoteProcess(id: string): Promise<void> {
    this.context.commit('setQuoteProcessBlank');
    this.context.commit('setQuoteProcessPending');
    try {
      const quoteProcess = await retrieveQuoteProcessById(id);
      this.context.commit('setQuoteProcess', quoteProcess)
      deconstructQuoteProcess(quoteProcess);
    } catch(e) {
      this.context.commit('setQuoteProcess', e)
    }
  }

  @Action
  async retrieveQuoteProcessCalcVariations(id: string): Promise<void> {
    this.context.commit('setQuoteProcessCalcVariationsBlank')
    this.context.commit('setQuoteProcessCalcVariationsPending')
    try {
      const variations = await retrieveCalcQuoteProcessVariations(id);
      this.context.commit('setQuoteProcessCalcVariations', variations)
    } catch (e) {
      this.context.commit('setQuoteProcessCalcVariations', e)
    }
  }

  @Action
  updateQuoteEmail(email: string): void {
    this.context.commit('setQuoteEmail', email);
  }

  @Action
  updateQuestionAnswers(payload: QuestionsStep): void {
    this.context.commit('setQuestionAnswers', {
      ...this.questionAnswers,
      ...payload
    })
  }

  @Action
  updateStepStatus(payload: { step: OrderedQuoteRouteNames, value: boolean }): void {
    this.context.commit('setStepCompleted', payload);
  }
}