import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';
import {VINStepFHVInfo, VINStepInsuranceInfo } from '@/@types/quote';

import { APIProperty, APIState } from '@/store/api'
import { getVINFHVInfo, getVINInsuranceInfo } from '@/store/importer/api'

@Module({ namespaced: true })
export default class QuoteVINVuexModule extends VuexModule {
  apiFHVInfo: APIProperty<VINStepFHVInfo> = APIState.state<VINStepFHVInfo>()
  apiInsuranceInfo: APIProperty<VINStepInsuranceInfo> = APIState.state<VINStepInsuranceInfo>()

  get fhvInfo(): VINStepFHVInfo | undefined {
    return this.apiFHVInfo.data
  }

  get insuranceInfo(): VINStepInsuranceInfo | undefined {
    return this.apiInsuranceInfo.data
  }

  get hasErrors(): boolean {
    return !!this.apiFHVInfo.error || !!this.apiInsuranceInfo.error
  }

  @Mutation
  setApiFHVInfoBlank(): void {
    this.apiFHVInfo = APIState.state<VINStepFHVInfo>();
  }

  @Mutation
  setApiInsuranceInfoBlank(): void {
    this.apiInsuranceInfo = APIState.state<VINStepInsuranceInfo>();
  }

  @Mutation
  setApiFHVInfoPending(): void {
    this.apiFHVInfo = APIState.setPending(this.apiFHVInfo)
  }

  @Mutation
  setApiInsuranceInfoPending(): void {
    this.apiInsuranceInfo = APIState.setPending(this.apiInsuranceInfo)
  }

  @Mutation
  setApiFHVInfo(payload: VINStepFHVInfo | Error): void {
    this.apiFHVInfo = APIState.update(this.apiFHVInfo, payload);
  }

  @Mutation
  setApiInsuranceInfo(payload: VINStepInsuranceInfo | Error): void {
    this.apiInsuranceInfo = APIState.update(this.apiInsuranceInfo, payload);
  }

  @Action
  async retrieveFHVInfo(vehicle_vin_number: string): Promise<void> {
    this.context.commit('setApiFHVInfoPending');
  
    try {
      const fhvInfo = await getVINFHVInfo(vehicle_vin_number.toUpperCase());
      this.context.commit('setApiFHVInfo', fhvInfo);
    } catch (e) {
      this.context.commit('setApiFHVInfo', e)
    }
  }

  @Action
  async retrieveInsuranceInfo(vin: string): Promise<void> {
    this.context.commit('setApiInsuranceInfoPending');
  
    try {
      const insuranceInfo = await getVINInsuranceInfo(vin.toUpperCase());
      this.context.commit('setApiInsuranceInfo', insuranceInfo);
    } catch (e) {
      this.context.commit('setApiInsuranceInfo', e)
    }
  }

  @Action
  resetFHVInfo(): void {
    this.context.commit('setApiFHVInfoBlank')
  }

  @Action
  resetInsuranceInfo(): void {
    this.context.commit('setApiInsuranceInfoBlank')
  }
}