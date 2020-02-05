import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';
import { QuestionsStep } from '@/@types/quote';

import { checkEmailExists as apiCheckEmailExists } from '@/store/users/api'

import { QuoteRouteNames } from '@/router/quote'

@Module({ namespaced: true })
export default class QuoteMainVuexModule extends VuexModule {
  internalEmailExist = false;
  internalQuestionAnswers: QuestionsStep = {}
  stepsCompleted = {
    [QuoteRouteNames.TLC]: false,
    [QuoteRouteNames.VIN]: false,
    [QuoteRouteNames.QUESTION_LONG_TLC]: false,
    [QuoteRouteNames.QUESTION_LONG_DMV]: false,
    [QuoteRouteNames.QUESTION_DRIVER_POINTS]: false,
    [QuoteRouteNames.QUESTION_FAULT_ACCIDENTS]: false,
    [QuoteRouteNames.QUESTION_DEFENSIVE_CERTIFICATE]: false,
    [QuoteRouteNames.QUESTION_ACCIDENT_AVOIDANCE]: false,
    [QuoteRouteNames.EMAIL]: false
  }

  get emailExists(): boolean {
    return this.internalEmailExist
  }

  get questionAnswers(): QuestionsStep {
    return this.internalQuestionAnswers
  }

  get stepCompletedByName(): (name: QuoteRouteNames) => boolean {
    return (name: QuoteRouteNames) => this.stepsCompleted[name];
  }

  @Mutation
  setEmailExists(value: boolean): void {
    this.internalEmailExist = value;
  }

  @Mutation
  setQuestionAnswers(payload: QuestionsStep): void {
    this.internalQuestionAnswers = {
      ...payload
    }
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
  updateQuestionAnswers(payload: QuestionsStep): void {
    this.context.commit('setQuestionAnswers', {
      ...this.internalQuestionAnswers,
      ...payload
    })
  }

  @Action
  updateStepStatus(payload: { step: QuoteRouteNames, value: boolean }): void {
    this.context.commit('setStepCompleted', payload);
  }
}