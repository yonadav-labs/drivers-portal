import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';
import { TLCStepLicenseName } from '@/@types/quote';

import { APIProperty, APIState } from '@/store/api'
import { getTLCLicenseName } from './api'

@Module({ namespaced: true })
export default class QuoteTLCVuexModule extends VuexModule {
  tlcLicenseNameProperty: APIProperty<TLCStepLicenseName> = APIState.state<TLCStepLicenseName>();

  get tlcStepLicenseName(): TLCStepLicenseName | undefined {
    return this.tlcLicenseNameProperty.data
  }

  get tlcLicenseNameError(): Error | undefined {
    return this.tlcLicenseNameProperty.error!
  }

  get tlcLicenseNameSuccess(): boolean {
    return this.tlcLicenseNameProperty.status === 'success';
  }

  get tlcLicenseNameValid(): boolean {
    return !!this.tlcStepLicenseName
  }

  @Mutation
  setTlcStepLicenseBlank(): void {
    this.tlcLicenseNameProperty = APIState.state<TLCStepLicenseName>();
  }

  @Mutation
  setTlcStepLicenseLoading(): void {
    this.tlcLicenseNameProperty = APIState.setPending(this.tlcLicenseNameProperty)
  }

  @Mutation
  setTlcStepLicense(payload: TLCStepLicenseName | Error ): void {
    this.tlcLicenseNameProperty = APIState.update(this.tlcLicenseNameProperty, payload)
  }

  @Action
  async retrieveTLCName(licenseNumber: string): Promise<void> {
    this.context.commit('setTlcStepLicenseLoading')
  
    try {
      const tlcLicenseName = await getTLCLicenseName(licenseNumber);
      this.context.commit('setTlcStepLicense', tlcLicenseName)
    } catch (e) {
      this.context.commit('setTlcStepLicense', e);
    }
  }

  @Action
  resetTlc(): void {
    this.context.commit('setTlcStepLicenseBlank')
  }
}
