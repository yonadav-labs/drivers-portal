<template>
  <quote-process-columns-layout>
    <quote-summary></quote-summary>
    <div class="questions">
      <banner
        title="Physical Coverage"
        text="If you want Physical (Collision and Comprehensive) Coverage, please select your desired Deductible."
        :active="focus=='physical'"
        :info="true"
      >
        <basic-select
          v-model="internalDeductible"
          :selected="internalDeductible"
          :options="PHYSICAL_OPTIONS"
          :default-option-value="-1"
          @focus="focus='physical'"
        ></basic-select>
      </banner>
      <div class="divider"></div>
      <banner
        title="Add Deposit"
        text="Choose the the deposit amount you would like to pay. This is due immediately."
        :active="focus=='deposit'"
      >
        <basic-select
          v-model="internalDeposit"
          :selected="internalDeposit"
          :options="DEPOSIT_OPTIONS"
          :default-option-value="0"
          :disabled="!isDeductibleSet"
          @focus="focus='deposit'"
        ></basic-select>
      </banner>
      <div class="divider"></div>
      <banner
        title="When would you like your policy to start? "
        text="Choose a date up to 20 days in advance."
        :active="focus=='date'"
      >
        <input-datepicker
          class="input"
          placeholder="Select date"
          v-model="internalDate"
          :disabled-dates="disabledDates"
          format="MMM d yyyy"
          :disabled="!isDeductibleSet || !isDepositSet"
          @focus="focus='date'">
        </input-datepicker>
      </banner>
      <div class="divider"></div>
      <banner
        title="Your insurance includes"
        text="The following coverages are mandated by the NYC Taxi & Limousine Commission."
      ></banner>
      <dropdown-info
        title="Bodily injury"
        price="$100,000 - $300,000"
      >
        Bodily Injury Liability insurance pays for injuries you cause to another driver if you are at-fault in the accident.
      </dropdown-info>
      <dropdown-info
        title="Property damage"
        price="$100,000"
      >
        Property Damage Liability insurance pays for damages to someone else's property after an accident you cause.
      </dropdown-info>
      <dropdown-info
        title="Uninsured motorist"
        price="$25,000 - $50,000"
      >
        Uninsured Motorist insurance pays you damages for any injury recieved from an uninsured, negligent driver.
      </dropdown-info>
      <dropdown-info
        title="Personal injury protection"
        price="$200,000"
      >
        Personal Injury Protection insurance covers medical expenses and can cover lost wages.
      </dropdown-info>
      <dropdown-info
        title="Aggregate no-fault"
        price="$200,000"
      >
        Aggregate No-Fault insurance can cover medical expensive and lost wages. As no fault insurance, because it is available regardless of who caused the accident.
      </dropdown-info>
    </div>
    <div slot="right-column">
      <div class="insurance-info">
        <p class="insurance-title">Your insurance</p>
        <div class="insurance-text">
          <span>Liability</span>
          <span>{{ liabilityText }}</span>
        </div>
        <div class="insurance-text">
          <div>
            <span>Physical coverage</span>
            <span class="insurance-price" v-if="hasDeductible">Deductible {{ internalDeductible | currency }}</span>
          </div>
          <span
            v-if="hasDeductible"
          >{{ physicalAmount| currency }}</span>
          <span v-else-if="internalDeductible == 0">$0</span>
          <span v-else>$-</span>
        </div>
        <div class="insurance-text insurance-text--total">
          <span>Total</span>
          <span>{{ total | currency }}</span>
        </div>
        <a href class="insurance-info--question" @click.prevent.stop="setShowPremium(true)">
          <icon-info size="16" class="insurance-info__icon icon--blue"></icon-info>How is my premium calculated?
        </a>
      </div>

      <div class="insurance-resume">
        <div class="insurance-estimated">
          <p>Monthly payment</p>
          <p class="estimated-price">{{ monthlyPaymentText }}</p>
          <span class="estimated-date">9 payments starting on
            <br>
            {{ firstPaymentDue }}
          </span>
        </div>
        <div class="insurance-estimated">
          <p>Deposit</p>
          <p class="estimated-price">{{ depositText }}</p>
          <span class="estimated-date">{{ isDepositSet ? `${internalDeposit}%`:'--%' }} of total price</span>
        </div>
      </div>
      <button
        class="insurance-action"
        :class="{'active': ctaEnabled}"
        :disabled="!ctaEnabled"
        @click="getPolicy"
      >Get Your Insurance Policy!
        <icon-arrow-right class="icon" size="16"></icon-arrow-right>
      </button>
    </div>
    <modal-premium 
      v-if="!!quoteProcess && showPremium"
      :tlc-name="quoteProcess.tlc_name"
      :tlc-number="quoteProcess.tlc_number"
      :has-defensive="quoteProcess.defensive_driving_certificate"
      :points="quoteProcess.driver_points_last_months"
      :accidents="quoteProcess.fault_accidents_last_months"
      :vehicle-vin="quoteProcess.vehicle_vin"
      :vehicle-owner="quoteProcess.vehicle_owner"
      :vehicle-plate="quoteProcess.license_plate"
      :vehicle-year="quoteProcess.vehicle_year"
      :base-name="quoteProcess.base_name"
      :base-number="quoteProcess.base_number"
      :insurance-name="quoteProcess.insurance_carrier_name"
      :insurance-policy="quoteProcess.insurance_policy_number"
      :deposit-option="internalDeposit"
      :deductible-option="internalDeductible"
      :variations="quoteProcessCalcVariations"
      :physical="selectedPhysical"
      :total="total"
      :monthly-payment="monthlyPayment"
      :deposit="deposit"
      :first-payment-due="firstPaymentDue"

      @close="setShowPremium(false)"
      ></modal-premium>
  </quote-process-columns-layout>
</template>

<script lang="ts">
import { Component, Vue, Watch, Prop } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class';

import { Route } from 'vue-router';

import { addDays, addMonths, format } from 'date-fns';

import Banner from '@/components/containers/banner.vue'
import BasicButton from '@/components/buttons/basic-button.vue'
import BasicSelect from '@/components/inputs/basic-select.vue'
import DropdownInfo from '@/components/containers/dropdown-info.vue'
import IconArrowRight from '@/components/icons/icon-arrow-right.vue'
import IconInfo from '@/components/icons/icon-info.vue'
import InputDatepicker from '@/components/inputs/input-datepicker.vue'
import ModalPremium from '@/apps/quote/components/modals/modal-premium.vue'
import QuoteProcessColumnsLayout from '@/apps/quote/components/layout/quote-process-columns-layout.vue'
import QuoteSummary from '@/apps/quote/components/containers/quote-summary.vue'

import { RouteName } from '@/router'
import { OrderedQuoteRouteName, QuoteProcessRouter } from '@/router/quote'

import { QuoteProcess, QuoteProcessCalcVariations, QuoteProcessVariationPhysical, QuoteProcessOptionsPayload } from '@/@types/quote';

import { currency, beautyCurrency } from '@/utils/text'


const quote = namespace('Quote')

// Ninth Step 
@Component({
  components: {
    Banner, BasicButton, BasicSelect, DropdownInfo, InputDatepicker, QuoteProcessColumnsLayout,
    IconArrowRight, IconInfo, QuoteSummary, ModalPremium
  },
  filters: {
    currency(value: number): string {
      return currency(value)
    }
  }
})
export default class StepQuote extends Vue {

  @Prop({ default: ''})
  quoteId!: string

  @quote.Getter
  magicLink!: string;

  @quote.Getter
  quoteProcess?: QuoteProcess

  @quote.Getter
  quoteProcessId?: string

  @quote.Getter
  quoteProcessCalcVariations?: QuoteProcessCalcVariations

  @quote.Action
  retrieveDeconstructQuoteProcess!: (id: string) => Promise<void>

  @quote.Action
  retrieveQuoteProcessCalcVariations!: (id: string) => Promise<void>

  @quote.Action
  updateQuoteProcessOptions!: (payload: QuoteProcessOptionsPayload) => Promise<void>

  @quote.Action
  updateQuoteProcessUser!: (userEmail: string) => Promise<void>

  DEPOSIT_OPTIONS = [
    {
      text: '15%',
      value: 15
    },
    {
      text: '20%',
      value: 20
    },
    {
      text: '25%',
      value: 25
    }
  ]

  PHYSICAL_OPTIONS = [
    {
      text: 'No',
      value: 0
    },
    {
      text: '$750',
      value: 750
    },
    {
      text: '$1,000',
      value: 1000
    },
    {
      text: '$1,500',
      value: 1500
    }
  ]

  internalDeductible = -1
  internalDeposit = 0
  internalDate = ''
  
  disabledDates = {
    to: new Date(),
    from: addDays(new Date(), 20)
  }

  focus = 'physical'
  showPremium = false;

  get ctaEnabled(): boolean {
    return this.isDeductibleSet && this.isDepositSet && this.internalDate !== ''
  }

  get hasDeductible(): boolean {
    return this.internalDeductible > 0;
  }

  get isDepositSet(): boolean {
    return this.internalDeposit > 0;
  }

  get isDeductibleSet(): boolean {
    return this.internalDeductible !== -1;
  }

  get monthlyPayment(): number {
    return (this.total * (1-(this.internalDeposit/100)))/9;
  }

  get deposit(): number {
    if (!this.isDepositSet) {
      return 0
    }
    return this.total * (this.internalDeposit/100)
  }

  get depositText(): string {
    return this.isDepositSet ? beautyCurrency(this.deposit):'$--'
  }

  get firstPaymentDue(): string {
    if (!this.internalDate) {
      return '--'
    }
    const selectedDate = new Date(this.internalDate)
    return format(addMonths(selectedDate, 3), 'MMM d, yyyy')
  }

  get liabilityText(): string {
    return !!this.quoteProcessCalcVariations ? currency(this.quoteProcessCalcVariations.liability_total):'$--'
  }

  get monthlyPaymentText(): string {
    return this.isDepositSet ? beautyCurrency(this.monthlyPayment):'$--'
  }

  get selectedPhysical(): QuoteProcessVariationPhysical | undefined {
    if (!!this.quoteProcessCalcVariations && this.hasDeductible) {
      return this.quoteProcessCalcVariations.deductible[this.internalDeductible]
    }
  }

  get physicalAmount(): number {
    return this.hasDeductible ? this.selectedPhysical!.physical_total:0
  }
  
  get total(): number {
    if (!this.quoteProcessCalcVariations) {
      return 0;
    }
    return this.quoteProcessCalcVariations.liability_total + this.physicalAmount
  }

  @Watch('internalDeductible')
  onPhysicalChange(val: string): void {
    if (!!val) {
      this.focus = 'deposit'
    }
  }

  @Watch('internalDeposit')
  onDepositChange(val: string): void {
    if (!!val) {
      this.focus = 'date'
    }
  }

  async beforeRouteEnter (to: Route, from: Route, next: any): Promise<void> {
    next(async (vm: StepQuote) => {
      if (!vm.quoteId) {
        vm.$router.replace(QuoteProcessRouter.getRouteByOrder(0))
      } else {
        if (!vm.quoteProcess) {
          await vm.retrieveDeconstructQuoteProcess(vm.quoteId);
          if (!vm.quoteProcess) {
            vm.$router.replace(QuoteProcessRouter.getRouteByOrder(0))
          }
        }

        if(!vm.quoteProcessCalcVariations) {
          await vm.retrieveQuoteProcessCalcVariations(vm.quoteId);
          if (!vm.quoteProcessCalcVariations) {
            vm.$router.replace(QuoteProcessRouter.getRouteByOrder(0))
          }
        }
      }
    })
  }

  async getPolicy(): Promise<void> {
    await this.updateQuoteProcessOptions({
      deposit: this.internalDeposit,
      deductible: this.hasDeductible ? this.internalDeductible:undefined,
      start_date: this.internalDate
    })
    if (this.quoteProcess && !!this.quoteProcess.deposit) {
      await this.updateQuoteProcessUser(this.quoteProcess.email)
      
      if (!!this.magicLink) {
        this.$router.push({ name: RouteName.MAGIC_LINK, params: { id: this.magicLink } })
      }
    }
  }

  setShowPremium(value: boolean): void {
    this.showPremium = value;
  }
}
</script>

<style lang='scss' scoped>
.divider {
  border-top: 2px dashed $grey-medium;
  margin: 1rem 0;
  width: 100%;
}

 .insurance-info {
  font-size: $fs-lg;
  padding: 1.875rem;

  .insurance-info--question {
    color: $blue;
    display: flex;
    font-weight: $fw-semibold;
    font-size: $fs-md;
  }

  .insurance-info__icon {
    margin-right: 0.5rem;
  }
}
.insurance-resume {
  background-color: rgba(241, 243, 245, 0.92);
  display: flex;
  justify-content: space-between;
  padding: 1.25rem;
  .insurance-estimated {
    background-color: $white;
    border-radius: 2px;
    text-align: center;
    display: flex;
    flex-direction: column;
    padding: 1rem 0.875rem 0.875rem;
    width: 9.813rem;
    span {
      font-size: $fs-lg;
    }
    p {
      text-align: center;
      &.estimated-price {
        color: $blue;
        font-size: $fs-xl;
        font-weight: $fw-semibold;
        margin-top: 1rem;
        margin-bottom: 1rem;
      }
    }
    .estimated-date {
      background-color: $grey-light;
      font-size: $fs-sm;
      margin: 0 auto;
      opacity: 0.5;
      padding: 0.5rem;
    }
  }
}
.insurance-action {
  background-color: $grey;
  border-radius: 0 0 8px 8px;
  color: $white;
  cursor: not-allowed;
  display: flex;
  justify-content: center;
  font-size: $fs-md;
  font-weight: $fw-semibold;
  text-align: center;
  text-decoration: none;
  padding: 1rem 0;
  width: 100%;
  .icon {
    color: $white;
    margin-left: 1rem;
  }
  &.active {
    background-image: linear-gradient(105deg, #fca011, #f76707);
    cursor: pointer;
  }
}
.insurance-title {
  font-size: $fs-md;
  font-weight: $fw-semibold;
  line-height: 1.22;
  text-transform: uppercase;
  padding-bottom: 1.875rem;
}
.insurance-text {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.25rem;
  > div {
    display: flex;
    flex-direction: column;
  }
  .insurance-price {
    color: $grey-darker;
    font-size: $fs-md;
    padding-top: 0.5rem;
  }
  &.insurance-text--total {
    span {
      font-weight: $fw-bold;
      line-height: 22px;
    }
  }
}

.questions {
  margin-top: 1rem;
}
</style>
