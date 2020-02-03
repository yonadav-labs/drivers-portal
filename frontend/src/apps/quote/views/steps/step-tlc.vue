<template>
  <quote-process-layout>
    <div class='form'>
      <p class='form__explain'>To start, we need your TLC number.</p>
        <form id='tlcForm' @submit.prevent.stop="onNext">
          <div class='form-input'>
            <div class='form-input__input'>
              <span class='form-input__label'>TLC license number</span>
              <basic-input
              id='tlcLicenseField'
              class='form-input__tlc'
              v-model="tlcValue"
              :minlength='6'
              :maxlength='7'
              type='text'
              placeholder='000000'>
              </basic-input>
            </div>
            <error-message class="error" v-if="!!tlcError" slot="error">We couldn't find any record. Please, try again</error-message>
          </div>
          <basic-button
            text='Next Step'
            :disabled="tlcValue.length < 6"
            :color='colorBlue'
          >
          <icon-arrow-right size='16' class='icon--blue'></icon-arrow-right>
          </basic-button>
      </form>
    </div>
  </quote-process-layout>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';

import { Getter, Action } from 'vuex-class';

import BasicButton from '@/components/buttons/basic-button.vue'
import BasicInput from '@/components/inputs/basic-input.vue'
import IconArrowRight from '@/components/icons/icon-arrow-right.vue'
import QuoteProcessLayout from '@/apps/quote/components/layout/quote-process-layout.vue'
import ErrorMessage from '@/components/error-message.vue'

import { Colors } from '@/utils/colors'
import { TLCStepLicenseName } from '../../../../@types/quote';


// First Step 

@Component({
  components: {
    QuoteProcessLayout, BasicButton, BasicInput, IconArrowRight,
    ErrorMessage
  }
})
export default class StepTLC extends Vue {

  @Getter('Quote/tlcLicenseName')
  tlcLicenseName?: TLCStepLicenseName

  @Getter('Quote/tlcLicenseNameError')
  tlcLicenseNameError?: Error

  @Getter('Quote/tlcLicenseNameSuccess')
  tlcLicenseNameSuccess!: boolean

  @Action('Quote/retrieveTLCName')
  retrieveTLCName!: (licenseNumber: string) => Promise<void>

  tlcValue = ''

  created(): void {
    this.tlcValue = this.tlcLicenseNumber || ''
  }

  get colorBlue(): string {
    return Colors.Blue
  }

  get tlcLicenseNumber(): string {
    return this.tlcLicenseName ? this.tlcLicenseName.license_number:''
  }

  get tlcError(): boolean {
    return !!this.tlcLicenseNameError
  }

  // @Watch('tlcLicenseNumber')
  // ontlcLicenseNumberChange(val?: string): void {
  //   this.tlcValue = this.tlcLicenseNumber || '';
  // }

  async onNext(): Promise<void> {
    await this.retrieveTLCName(this.tlcValue);
    if (this.tlcLicenseNameSuccess) {
      this.$router.push({ name: 'quoteTlcConfirm' })
    }
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
    padding: 0.75rem 2rem;

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
}
</style>
