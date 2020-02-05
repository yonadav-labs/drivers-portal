import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';
import { QuestionsStep } from '@/@types/quote';

import { APIProperty, APIState } from '@/store/api'

import { QuoteRouteNames } from '@/router/quote'

@Module({ namespaced: true })
export default class QuoteMainVuexModule extends VuexModule {
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

  get questionAnswers(): QuestionsStep {
    return this.internalQuestionAnswers
  }

  get stepCompletedByName(): (name: QuoteRouteNames) => boolean {
    return (name: QuoteRouteNames) => this.stepsCompleted[name];
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