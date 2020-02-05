import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';

import { QuestionsStep, QuoteProcess } from '@/@types/quote';

import { APIProperty, APIState } from '@/store/api'
import {
  createQuoteProcess, retrieveQuoteProcessById, updateQuoteProcess
} from '@/store/quote/api'

import { checkEmailExists as apiCheckEmailExists } from '@/store/users/api'

import { QuoteRouteNames, QuoteProcessRouter } from '@/router/quote'

import { buildQuoteProcessPayload, deconstructQuoteProcess } from './helpers'

@Module({ namespaced: true })
export default class QuoteMainVuexModule extends VuexModule {
  apiQuoteProcess: APIProperty<QuoteProcess> = APIState.state<QuoteProcess>();
  internalEmailExist = false;
  internalQuestionAnswers: QuestionsStep = {}
  internalQuoteEmail = '';
  stepsCompleted = {
    [QuoteRouteNames.TLC]: false,
    [QuoteRouteNames.VIN]: false,
    [QuoteRouteNames.QUESTION_LONG_TLC]: false,
    [QuoteRouteNames.QUESTION_LONG_DMV]: false,
    [QuoteRouteNames.QUESTION_DRIVER_POINTS]: false,
    [QuoteRouteNames.QUESTION_FAULT_ACCIDENTS]: false,
    [QuoteRouteNames.QUESTION_DEFENSIVE_CERTIFICATE]: false,
    [QuoteRouteNames.QUESTION_ACCIDENT_AVOIDANCE]: false,
    [QuoteRouteNames.EMAIL]: false,
    [QuoteRouteNames.QUOTE]: false
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

  get stepCompletedByName(): (name: QuoteRouteNames) => boolean {
    return (name: QuoteRouteNames) => this.stepsCompleted[name];
  }

  @Mutation
  setEmailExists(value: boolean): void {
    this.internalEmailExist = value;
  }

  @Mutation
  setMultipleStepsCompleted(payload: { step: QuoteRouteNames, value: boolean }): void {
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
  setStepCompleted(payload: { step: QuoteRouteNames, value: boolean }): void {
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
  updateStepStatus(payload: { step: QuoteRouteNames, value: boolean }): void {
    this.context.commit('setStepCompleted', payload);
  }
}