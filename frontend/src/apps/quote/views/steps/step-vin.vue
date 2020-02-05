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
                <error-message class="error" v-if="hasErrors" slot="error">We couldn't find any record. Please, try again</error-message>
            </div>
          </div>
          <basic-button
            text='Next Step'
            :disabled="vinValue.length < 17"
            :color='colorBlue'
            >
            <icon-arrow-right size='16' class='icon--blue'></icon-arrow-right>
          </basic-button>    
      </form>
    </div>
    <div v-else class="vin-container">
      <p class="vin-container__explain">
        We found this car registered under the VIN Number. Is that the car you want to insure?
      </p>
      <div class="vin-content vin-content--success">
        <div class="search-result">
          <p class="search-result__label">VIN</p>
          <p class="search-result__result">{{ fhvInfo.vehicle_vin }}</p>
        </div>
        <div class="search-result-divider"></div>
        <div class="search-result">
          <p class="search-result__label">Vehicle License Plate</p>
          <p class="search-result__result">{{ fhvInfo.license_plate }}</p>
        </div>
        <div class="search-result">
          <p class="search-result__label">Vehicle Owner</p>
          <p class="search-result__result">{{ prettifyName(fhvInfo.vehicle_owner) }}</p>
        </div>
        <div class="search-result">
          <p class="search-result__label">Current Insurance and Policy</p>
          <p class="search-result__result">{{ prettifyName(insuranceInfo.insurance_carrier_name) }} ({{ insuranceInfo.insurance_policy_number }})</p>
        </div>
        <div class="search-result">
          <p class="search-result__label">Base Name and Number</p>
          <p class="search-result__result">{{ fhvInfo.base_name }} ({{ fhvInfo.base_number }})</p>
        </div>  
      </div>
      <div class="vin-container__yes-no">
        <basic-button
          text='Yes'
          :color='colorBlue'
          @click.stop.prevent="onIsMe"
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
import { Route } from 'vue-router';

import BasicButton from '@/components/buttons/basic-button.vue'
import BasicInput from '@/components/inputs/basic-input.vue'
import IconArrowRight from '@/components/icons/icon-arrow-right.vue'
import IconCheck from '@/components/icons/icon-check.vue'
import IconCross from '@/components/icons/icon-cross.vue'
import QuoteProcessLayout from '@/apps/quote/components/layout/quote-process-layout.vue'
import ErrorMessage from '@/components/error-message.vue'

import { capitalize } from '@/utils/text'
import { Colors } from '@/utils/colors'

import { TLCStepLicenseName, VINStepFHVInfo, VINStepInsuranceInfo } from '../../../../@types/quote';

import { QuoteRouteNames, QuoteProcessRouter } from '@/router/quote'

// Second Step 

const quote = namespace('Quote')
const quoteTLC = namespace('QuoteTlc')
const quoteVIN = namespace('QuoteVin')

@Component({
  components: {
    QuoteProcessLayout, BasicButton, BasicInput, IconArrowRight,
    ErrorMessage, IconCheck, IconCross
  }
})
export default class StepVIN extends Vue {

  @quote.Getter
  stepCompletedByName!: (route: QuoteRouteNames) => boolean

  @quoteTLC.Getter
  tlcStepLicenseName?: TLCStepLicenseName

  @quoteVIN.Getter
  hasErrors!: boolean

  @quoteVIN.Getter
  fhvInfo: VINStepFHVInfo | undefined
  
  @quoteVIN.Getter
  insuranceInfo: VINStepInsuranceInfo | undefined

  @quote.Action
  updateStepStatus!: (payload: { step: QuoteRouteNames, value: boolean }) => void;

  @quoteVIN.Action
  retrieveFHVInfo!: (vehicle_vin_number: string) => void

  @quoteVIN.Action
  retrieveInsuranceInfo!: (vin: string) => void

  @quoteVIN.Action
  resetFHVInfo!: () => void;
  
  @quoteVIN.Action
  resetInsuranceInfo!: () => void;

  vinValue = ''

  get colorBlue(): string {
    return Colors.Blue
  }

  get colorOrange(): string {
    return Colors.Orange
  }

  get success(): boolean {
    return !!this.fhvInfo && !!this.insuranceInfo
  }

  onNext(): void {
    this.retrieveFHVInfo(this.vinValue);
    this.retrieveInsuranceInfo(this.vinValue);
  }

  onIsMe(): void {
    this.updateStepStatus({ step: this.$route.name! as QuoteRouteNames, value: true});
    this.$router.push(QuoteProcessRouter.nextRoute(this.$route.name! as QuoteRouteNames))
  }

  onNotMe(): void {
    this.resetState();
  }

  prettifyName(name: string): string {
    return capitalize(name)
  }

  resetState(): void {
    this.updateStepStatus({ step: this.$route.name! as QuoteRouteNames, value: false});
    this.resetFHVInfo();
    this.resetInsuranceInfo();
    this.vinValue = ''
  }

  beforeRouteEnter (to: Route, from: Route, next: any): void {
    next((vm: StepVIN) => {
      if (!from.name || QuoteProcessRouter.isBefore(from.name as QuoteRouteNames, vm.$route.name! as QuoteRouteNames)) {
        vm.resetState();
      }

      if (!vm.stepCompletedByName(QuoteProcessRouter.previousRouteName(vm.$route.name! as QuoteRouteNames))) {
        vm.resetState();
        vm.$router.replace(QuoteProcessRouter.previousRoute(vm.$route.name! as QuoteRouteNames));
      }
    })
  }
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
    flex-direction: row-reverse;
    justify-content: center;

    > button {
      flex-grow: 1;
    }
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
