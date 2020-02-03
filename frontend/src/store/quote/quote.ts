import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';
import { TLCStepLicenseName } from '@/@types/quote';

@Module
export default class QuoteVuexModule extends VuexModule {
  tlcStepLicenseName: TLCStepLicenseName = {} as TLCStepLicenseName;

  get tlcLicenseName(): TLCStepLicenseName {
    return {
      ...this.tlcStepLicenseName
    }
  }

  @Mutation
  setTlcStepLicenseName(payload: TLCStepLicenseName) {
    this.tlcStepLicenseName = {
      ...payload
    }
  }

  @Action
  retrieveTLCName(licenseNumber: string): void {

  }
}
