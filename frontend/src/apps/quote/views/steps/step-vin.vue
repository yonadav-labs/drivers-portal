<template>
  <quote-process-layout>
    VIN
  </quote-process-layout>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';

import { Getter, Action } from 'vuex-class';

import BasicButton from '@/components/buttons/basic-button.vue'
import BasicInput from '@/components/inputs/basic-input.vue'
import IconArrowRight from '@/components/icons/icon-arrow-right.vue'
import IconCheck from '@/components/icons/icon-check.vue'
import IconCross from '@/components/icons/icon-cross.vue'
import QuoteProcessLayout from '@/apps/quote/components/layout/quote-process-layout.vue'
import ErrorMessage from '@/components/error-message.vue'

import { Colors } from '@/utils/colors'
import { TLCStepLicenseName } from '../../../../@types/quote';


// First Step 

@Component({
  components: {
    QuoteProcessLayout, BasicButton, BasicInput, IconArrowRight,
    ErrorMessage, IconCheck, IconCross
  }
})
export default class StepVIN extends Vue {

  @Getter('Quote/tlcStepLicenseName')
  tlcStepLicenseName?: TLCStepLicenseName

  @Getter('Quote/tlcLicenseNameError')
  tlcLicenseNameError?: Error

  @Getter('Quote/tlcLicenseNameSuccess')
  tlcLicenseNameSuccess!: boolean

  @Action('Quote/retrieveTLCName')
  retrieveTLCName!: (licenseNumber: string) => Promise<void>

  @Action('Quote/resetTlc')
  resetTlc!: () => void

  tlcValue = ''

  created(): void {
    this.tlcValue = this.tlcLicenseNumber || ''
  }

  get colorBlue(): string {
    return Colors.Blue
  }

  get colorOrange(): string {
    return Colors.Orange
  }

  get isConfirmStep(): boolean {
    return this.tlcLicenseName.length > 0
  }

  get tlcLicenseNumber(): string {
    return this.tlcStepLicenseName ? this.tlcStepLicenseName.license_number:''
  }

  get tlcLicenseName(): string {
    return this.tlcStepLicenseName ? this.tlcStepLicenseName.name:''
  }

  get tlcError(): boolean {
    return !!this.tlcLicenseNameError
  }

  async onNext(): Promise<void> {
    await this.retrieveTLCName(this.tlcValue);
  }

  onNotMe(): void {
    this.resetTlc();
    this.tlcValue = '';
  }

  prettifyName(name: string): string {
    return name.split(',').map(x => x.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join(' ')).join(', ')
  }
}
</script>

<style lang='scss' scoped>
.form {
  padding: 1.875rem 5.625rem 1.75rem;
  text-align: center;

  .form__explain {
    line-height: 1.5;
    font-size: $fs-lg;
    margin-left: auto;
    margin-right: auto;

    span {
      font-weight: $fw-semibold;
    }
  }


  .form-input {
    background-color: rgba(206, 212, 218, 0.2);
    border-radius: 8px;
    margin: 1.25rem auto;

    .form-input__container {
      padding: 0.75rem 2rem;
    }

    .form-input__input {
      align-items: center;
      display: flex;
      justify-content: space-between;
    }

    .form-input__label {
      font-size: $fs-lg;
      font-weight: $fw-semibold;
      opacity: 0.8;
    }
    .form-input__tlc {
      width: 8rem;

      .error {
        font-size: $fs-xs;
        margin-top: 0.5rem;
      }
    }
  }

  .form__yes-no {
    align-items: center;
    display: flex;
    justify-content: center;
  }

  .form__result {
    background-color: rgba(206,212,218,0.4);
    border-bottom-left-radius: 8px; 
    border-bottom-right-radius: 8px; 
    line-height: 28px;
    padding: 1.25rem 1rem;
    text-align: center;

    span {
      font-weight: $fw-semibold;
    }
  }
}
</style>
