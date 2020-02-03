<template>
  <quote-process-layout>
    <div class='vin-container' v-if="!success">
        <p class='vin-container__explain'>Please, enter your vehicle's VIN</p>
        <form id='vinForm' @submit.prevent.stop="onNext">
          <div class="vin-content form-input">
            <div class="form-input__container">
                <div class='form-input__input'>
                  <span class='form-input__label'>VIN</span>
                  <basic-input
                    id='vinLicenseField'
                    class='form-input__vin'
                    v-model="vinValue"
                    :minlength='17'
                    :maxlength='17'
                    type='text'
                    placeholder='00000000000000000'
                    icon="car"
                    >
                    </basic-input>
                </div>
                <error-message class="error" v-if="!!vinError" slot="error">We couldn't find any record. Please, try again</error-message>
            </div>
          </div>
          <basic-button
            text='Next Step'
            :disabled="vinValue.length < 17"
            :color='colorBlue'
            >
            <icon-arrow-right size='16' class='icon--blue'></icon-arrow-right>
          </basic-button>
          <!-- <div class="form__yes-no" v-else>
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

          </div>         -->
      </form>
    </div>
    <div v-else class="vin-container">
      <p class="vin-container__explain">
        We found this car registered under the VIN Number. Is that the car you want to insure?
      </p>
      <div class="vin-content vin-content--success">
        <div class="search-result">
          <p class="search-result__label">VIN</p>
          <p class="search-result__result">2454654213775421</p>
        </div>
        <div class="search-result-divider"></div>
        <div class="search-result">
          <p class="search-result__label">Vehicle License Plate</p>
          <p class="search-result__result">T927007C</p>
        </div>
        <div class="search-result">
          <p class="search-result__label">Vehicle Owner</p>
          <p class="search-result__result">Erlich Bachman</p>
        </div>
        <div class="search-result">
          <p class="search-result__label">Current Insurance and Policy</p>
          <p class="search-result__result">Hereford (580398)</p>
        </div>
        <div class="search-result">
          <p class="search-result__label">Base Name and Number</p>
          <p class="search-result__result">G.T.N.Y. CAR SERVICE, INC. (B02847)</p>
        </div>
      </div>
      <div class="vin-container__yes-no">
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
import QuoteProcessLayout from '@/apps/quote/components/layout/quote-process-layout.vue'
import ErrorMessage from '@/components/error-message.vue'

import { Colors } from '@/utils/colors'
import { TLCStepLicenseName } from '../../../../@types/quote';


const quoteTLC = namespace('QuoteTlc')

// Second Step 

@Component({
  components: {
    QuoteProcessLayout, BasicButton, BasicInput, IconArrowRight,
    ErrorMessage, IconCheck, IconCross
  }
})
export default class StepVIN extends Vue {

  @quoteTLC.Getter
  tlcStepLicenseName?: TLCStepLicenseName

  success = false
  vinError = true
  vinValue = ''


  get colorBlue(): string {
    return Colors.Blue
  }

  get colorOrange(): string {
    return Colors.Orange
  }

  created(): void {
    if (!this.tlcStepLicenseName) {
      this.$router.push({ name: 'quoteTlc' })
    }
  }

  // @Getter('Quote/tlcLicenseNameError')
  // tlcLicenseNameError?: Error

  // @Getter('Quote/tlcLicenseNameSuccess')
  // tlcLicenseNameSuccess!: boolean

  // @Action('Quote/retrieveTLCName')
  // retrieveTLCName!: (licenseNumber: string) => Promise<void>

  // @Action('Quote/resetTlc')
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
  // }

  // onIsMe(): void {
  //   this.$router.push({ name: 'quoteVin' })
  // }

  // prettifyName(name: string): string {
  //   return name.split(',').map(x => x.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join(' ')).join(', ')
  // }
}
</script>

<style lang='scss' scoped>
.vin-container {
  padding: 1.875rem 5.625rem 1.75rem;
  text-align: center;

  .vin-container__explain {
    line-height: 1.5;
    font-size: $fs-lg;
    margin-left: auto;
    margin-right: auto;

    span {
      font-weight: $fw-semibold;
    }
  }

  .vin-container__yes-no {
    align-items: center;
    display: flex;
    flex: 1;
    flex-direction: row-reverse;
    justify-content: center;
  }

  .vin-content {
    background-color: rgba(206, 212, 218, 0.2);
    border-radius: 8px;
    margin: 1.25rem auto;

    &.vin-content--success {
      padding: 1.25rem 1.5rem;
      text-align: left;
    }
  }

  .form-input {

    .form-input__container {
      padding: 0.75rem 2rem;
    }

    .form-input__input {
      align-items: center;
      display: flex;
      justify-content: space-around;
    }

    .form-input__label {
      font-size: $fs-lg;
      font-weight: $fw-semibold;
      opacity: 0.8;
    }
    .form-input__vin {
      width: 15rem;

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

  .search-result {

    .search-result__label {
      color: $grey-darker;
      line-height: 24px;
    }

    .search-result__result {
      color: $blue-dark;
      font-size: $fs-lg;
      font-weight: $fw-semibold;
      line-height: 24px;
      opacity: 0.8;
    }
    
    &:not(:first-child) {
      margin-top: 0.75rem;
    }
  }

  .search-result-divider {
    border: 1px solid $grey;
    margin-bottom: 1rem;
    margin-top: 1rem;
  }
}
</style>
