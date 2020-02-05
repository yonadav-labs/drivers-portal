<template>
  <quote-process-layout>
    <div class='form'>
        <p class='form__explain'>Great! We just need your <span>email</span> to verify.</p>
        <form id='emailForm' @submit.prevent.stop="onNext">
          <div class="form-input">
            <div class="form-input__container">
                <div class='form-input__input' ref="input">
                  <span class='form-input__label'>Email address</span>
                  <basic-input
                    id='tlcLicenseField'
                    class='form-input__email'
                    v-model="emailValue"
                    type='email'
                    placeholder='your.email-here@email.com'
                    icon="id-card"
                    :required="true"
                    @valid="onValidChange"
                    >
                    </basic-input>
                </div>
                <error-message class="error" v-if="emailExists" slot="error">This email is already registered as user</error-message>
            </div>
          </div>
          <basic-button
            text='Next Step'
            :disabled="!emailValid"
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

import { Getter, Action, namespace } from 'vuex-class';

import BasicButton from '@/components/buttons/basic-button.vue'
import BasicInput from '@/components/inputs/basic-input.vue'
import IconArrowRight from '@/components/icons/icon-arrow-right.vue'
import QuoteProcessLayout from '@/apps/quote/components/layout/quote-process-layout.vue'
import ErrorMessage from '@/components/error-message.vue'

import { Colors } from '@/utils/colors'
import { capitalize } from '@/utils/text'

import { TLCStepLicenseName } from '../../../../@types/quote';

import { QuoteRouteNames, QuoteProcessRouter } from '@/router/quote'


const quote = namespace('Quote')
const quoteTLC = namespace('QuoteTlc')

// Ninth Step 
@Component({
  components: {
    QuoteProcessLayout, BasicButton, BasicInput, IconArrowRight,
    ErrorMessage
  }
})
export default class StepEmail extends Vue {

  @quote.Getter
  emailExists!: boolean

  @quote.Action
  checkEmailExists!: (email: string) => Promise<void>

  get colorBlue(): string {
    return Colors.Blue
  }

  emailValid = false;
  emailValue = '';

  onValidChange(value: boolean): void {
    this.emailValid = value;
  }

  async onNext(): Promise<void> {
    await this.checkEmailExists(this.emailValue);
    if (this.emailExists) {
      console.log("Exists")
    } else {
      console.log("Not exist")
    }
  }


  // @quoteTLC.Getter
  // tlcStepLicenseName?: TLCStepLicenseName

  // @quoteTLC.Getter
  // tlcLicenseNameError?: Error

  // @quoteTLC.Getter
  // tlcLicenseNameSuccess!: boolean

  // @quote.Action
  // updateStepStatus!: (payload: { step: QuoteRouteNames, value: boolean }) => void;

  // @quoteTLC.Action
  // retrieveTLCName!: (licenseNumber: string) => Promise<void>

  // @quoteTLC.Action
  // resetTlc!: () => void

  // tlcValue = ''

  // created(): void {
  //   this.tlcValue = this.tlcLicenseNumber || ''
  // }

  // get colorBlue(): string {
  //   return Colors.Blue
  // }

  // get colorOrange(): string {
  //   return Colors.Orange
  // }

  // get isConfirmStep(): boolean {
  //   return this.tlcLicenseName.length > 0
  // }

  // get tlcLicenseNumber(): string {
  //   return this.tlcStepLicenseName ? this.tlcStepLicenseName.license_number:''
  // }

  // get tlcLicenseName(): string {
  //   return this.tlcStepLicenseName ? this.tlcStepLicenseName.name:''
  // }

  // get tlcError(): boolean {
  //   return !!this.tlcLicenseNameError
  // }

  // async onNext(): Promise<void> {
  //   await this.retrieveTLCName(this.tlcValue);
  // }

  // onNotMe(): void {
  //   this.resetTlc();
  //   this.tlcValue = '';
  //   this.updateStepStatus({ step: this.$route.name! as QuoteRouteNames, value: false});
  // }

  // onIsMe(): void {
  //   this.updateStepStatus({ step: this.$route.name! as QuoteRouteNames, value: true});
  //   this.$router.push(QuoteProcessRouter.nextRoute(this.$route.name! as QuoteRouteNames))
  // }

  // prettifyName(name: string): string {
  //   return capitalize(name)
  // }


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
    text-align: left;

    .form-input__container {
      padding: 1.25rem 2.5rem;
    }

    .form-input__input {
      align-items: flex-start;
      display: flex;
      flex-direction: column;
      justify-content:flex-start;
    }

    .form-input__label {
      font-size: $fs-lg;
      font-weight: $fw-semibold;
      margin-bottom: 0.5rem;
      opacity: 0.8;
    }
    .form-input__email {
      width: 100%;

      .error {
        font-size: $fs-xs;
        margin-top: 0.5rem;
      }
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
