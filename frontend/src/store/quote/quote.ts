import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

import { 
  QuestionsStep, QuoteProcess, QuoteSoftFallout,
  QuoteProcessCalcVariations,
  QuoteProcessOptionsPayload
} from '@/@types/quote';

import { APIProperty, APIState } from '@/store/api'
import {
  createQuoteProcess, retrieveQuoteProcessById, updateQuoteProcess,
  createQuoteSoftFallout, retrieveCalcQuoteProcessVariations,
  updateQuoteProcessOptions, updateQuoteProcessUser
} from '@/store/quote/api'

import { checkEmailExists as apiCheckEmailExists } from '@/store/users/api'

import { OrderedQuoteRouteName } from '@/router/quote'

import { buildQuoteProcessPayload, deconstructQuoteProcess } from './helpers'

@Module({ namespaced: true })
export default class QuoteMainVuexModule extends VuexModule {
  apiQuoteProcess: APIProperty<QuoteProcess> = APIState.state<QuoteProcess>();
  apiQuoteSoftFallout: APIProperty<QuoteSoftFallout> = APIState.state<QuoteSoftFallout>();
  apiQuoteProcessCalcVariations: APIProperty<QuoteProcessCalcVariations> = APIState.state<QuoteProcessCalcVariations>();
  internalEmailExist = false;
  internalQuestionAnswers: QuestionsStep = {}
  internalQuoteEmail = '';
  loginMagicLink = '';
  stepsCompleted = {
    [OrderedQuoteRouteName.TLC]: false,
    [OrderedQuoteRouteName.VIN]: false,
    [OrderedQuoteRouteName.QUESTION_LONG_TLC]: false,
    [OrderedQuoteRouteName.QUESTION_LONG_DMV]: false,
    [OrderedQuoteRouteName.QUESTION_DRIVER_POINTS]: false,
    [OrderedQuoteRouteName.QUESTION_FAULT_ACCIDENTS]: false,
    [OrderedQuoteRouteName.QUESTION_DEFENSIVE_CERTIFICATE]: false,
    [OrderedQuoteRouteName.QUESTION_ACCIDENT_AVOIDANCE]: false,
    [OrderedQuoteRouteName.EMAIL]: false,
    [OrderedQuoteRouteName.QUOTE]: false
  }

  get emailExists(): boolean {
    return this.internalEmailExist
  }

  get magicLink(): string {
    return this.loginMagicLink
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

  get stepCompletedByName(): (name: OrderedQuoteRouteName) => boolean {
    return (name: OrderedQuoteRouteName) => this.stepsCompleted[name];
  }

  @Mutation
  setEmailExists(value: boolean): void {
    this.internalEmailExist = value;
  }

  @Mutation
  setMultipleStepsCompleted(payload: { step: OrderedQuoteRouteName, value: boolean }): void {
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
  setQuoteProcessPartial(payload: QuoteProcess): void {
    this.apiQuoteProcess = APIState.patch(this.apiQuoteProcess, payload)
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
  setLoginMagicLink(magicLink: string): void {
    this.loginMagicLink = magicLink;
  }

  @Mutation
  setStepCompleted(payload: { step: OrderedQuoteRouteName, value: boolean }): void {
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
  async retrieveDeconstructQuoteProcess(id: string): Promise<void> {
    await this.context.dispatch('retrieveQuoteProcess', id)
    if (this.quoteProcess) {
      deconstructQuoteProcess(this.quoteProcess); 
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
  updateStepStatus(payload: { step: OrderedQuoteRouteName, value: boolean }): void {
    this.context.commit('setStepCompleted', payload);
  }

  @Action
  async updateQuoteProcessOptions(payload: QuoteProcessOptionsPayload): Promise<void> {
    this.context.commit('setQuoteProcessPending');

    try {
      const options = await updateQuoteProcessOptions(this.quoteProcessId!, payload)
      this.context.commit('setQuoteProcessPartial', options)
    } catch(e) {
      this.context.commit('setQuoteProcessPartial', e)
    }
  }

  @Action
  async updateQuoteProcessUser(userEmail: string): Promise<void> {
    this.context.commit('setQuoteProcessPending');
    this.context.commit('setLoginMagicLink', '')

    try {
      const { email, magic_link } = await updateQuoteProcessUser(this.quoteProcessId!, userEmail)
      this.context.commit('setQuoteProcessPartial', { email })
      this.context.commit('setLoginMagicLink', magic_link)
    } catch (e) {
      this.context.commit('setQuoteProcessPartial', e)
    }
  }
}