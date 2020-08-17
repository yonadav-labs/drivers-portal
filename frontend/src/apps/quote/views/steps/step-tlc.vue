<template>
  <quote-process-layout>
    <quote-summary></quote-summary>
    <div class='form'>
        <p class='form__explain'>To start, we need your TLC number.</p>
        <form id='tlcForm' @submit.prevent.stop="onNext">
          <div class="form-input">
            <div class="form-input__container">
                <div class='form-input__input'>
                  <span class='form-input__label'>TLC license number</span>
                  <basic-input
                    id='tlcLicenseField'
                    class='form-input__tlc'
                    v-model="tlcValue"
                    :minlength='6'
                    :maxlength='7'
                    type='text'
                    placeholder='000000'
                    :readonly="isConfirmStep"
                    icon="id-card"
                    >
                    </basic-input>
                </div>
                <error-message class="error" v-if="!!tlcError" slot="error">We couldn't find any record. Please, try again</error-message>
            </div>
            <div class="form__result" v-if="isConfirmStep">
              We found <span>{{ prettifyName(tlcLicenseName) }}</span> associated with that TLC Number. Are you this driver?
            </div>
          </div>
          <basic-button
            v-if="!isConfirmStep"
            text='Next Step'
            :disabled="tlcValue.length < 6"
            :color='colorBlue'
            >
            <icon-arrow-right size='16' class='icon--blue'></icon-arrow-right>
          </basic-button>
          <div class="form__yes-no" v-else>
            <basic-button
              @click.stop.prevent="onIsMe"
              text='Yes'
              :color='colorBlue'
              >
              <icon-check size='16' class='icon--blue'></icon-check>
            </basic-button>
            <basic-button
              text='No'
              :color='colorOrange'
              @click.stop.prevent="onNotMe"
              >
              <icon-cross size='16' class='icon--orange'></icon-cross>
            </basic-button>
          </div>        
      </form>
    </div>
  </quote-process-layout>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class';

import BasicButton from '@/components/buttons/basic-button.vue'
import BasicInput from '@/components/inputs/basic-input.vue'
import IconArrowRight from '@/components/icons/icon-arrow-right.vue'
import IconCheck from '@/components/icons/icon-check.vue'
import IconCross from '@/components/icons/icon-cross.vue'
import QuoteProcessLayout from '@/components/layout/quote-process-layout.vue'
import ErrorMessage from '@/components/error-message.vue'
import QuoteSummary from '@/apps/quote/components/containers/quote-summary.vue'

import { Colors } from '@/utils/colors'
import { capitalize } from '@/utils/text'

import { TLCStepLicenseName } from '../../../../@types/quote';

import { ExtraQuoteRouteNames, OrderedQuoteRouteName, QuoteProcessRouter } from '@/router/quote'


const quote = namespace('Quote')
const quoteTLC = namespace('QuoteTlc')

// First Step 

@Component({
  components: {
    QuoteProcessLayout, BasicButton, BasicInput, IconArrowRight,
    ErrorMessage, IconCheck, IconCross, QuoteSummary
  }
})
export default class StepTLC extends Vue {

  @quoteTLC.Getter
  tlcStepLicenseName?: TLCStepLicenseName

  @quoteTLC.Getter
  tlcLicenseNameError?: Error

  @quoteTLC.Getter
  tlcLicenseNameSuccess!: boolean

  @quote.Action
  updateStepStatus!: (payload: { step: string, value: boolean }) => void;

  @quoteTLC.Action
  retrieveTLCName!: (licenseNumber: string) => Promise<void>

  @quoteTLC.Action
  resetTlc!: () => void

  attempts = 0
  tlcValue = ''

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
    return this.tlcStepLicenseName ? this.tlcStepLicenseName.tlc_number:''
  }

  get tlcLicenseName(): string {
    return this.tlcStepLicenseName ? this.tlcStepLicenseName.tlc_name:''
  }

  get tlcError(): boolean {
    return !!this.tlcLicenseNameError
  }

  async onNext(): Promise<void> {
    EF.conversion({
      aid: 122,
    });

    await this.retrieveTLCName(this.tlcValue);
    if (this.tlcError) {
      this.attempts++;
    }
  }

  @Watch('attempts')
  onAttemptsChange(): void {
    if (this.attempts >= 2) {
      this.$router.replace({ name: ExtraQuoteRouteNames.SOFT_FALLOUT })
    }
  }

  onNotMe(): void {
    this.resetTlc();
    this.tlcValue = '';
    this.updateStepStatus({ step: this.$route.name!, value: false});
    this.attempts++;
  }

  onIsMe(): void {
    this.updateStepStatus({ step: this.$route.name!, value: true});
    this.$router.push(QuoteProcessRouter.nextRoute(this.$route.name!))
  }

  prettifyName(name: string): string {
    return capitalize(name)
  }

  created(): void {
    this.tlcValue = this.tlcLicenseNumber || ''
    this.onAttemptsChange();
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
    background-color: $grey-opacity;
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
      width: 8.5rem;

      .error {
        font-size: $fs-xs;
        margin-top: 0.5rem;
      }
    }
  }

  .form__yes-no {
    align-items: center;
    display: flex;
    flex-direction: row-reverse;
    justify-content: center;
    
    > button {
      flex-grow: 1;
    }
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
