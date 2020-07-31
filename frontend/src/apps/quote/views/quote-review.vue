<template>
  <quote-process-columns-layout v-if="!!quoteProcessPayment" :hide-breadcrumbs="true" :on-back="back">
    <quote-summary></quote-summary>
    <div class="questions">
      <div class="questions__result">
        <p class="questions__title">Deposit</p>
        <p class="questions__value">{{ quoteDeposit }}%</p>
      </div>
      <div class="divider"></div>
      <div class="questions__result">
        <p class="questions__title">Desired Policy Start Date</p>
        <p class="questions__value">{{ formatDate(quoteStartDate) }}</p>
      </div>
      <div class="divider"></div>
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
        <div class="insurance-text insurance-text--total">
          <span>Total</span>
          <span>{{ prp | currency }}</span>
        </div>
        <a href class="insurance-info--question" @click.prevent.stop="setShowPremium(true)">
          <icon-info size="16" class="insurance-info__icon icon--blue"></icon-info>How is my premium calculated?
        </a>
      </div>

      <div class="insurance-resume">
        <div class="monthly-payment-wrapper">
          <MonthlyPayment :qrsf="total" :deposit="deposit" :internalDeposit="quoteDeposit" :internalDate="quoteStartDate" />
        </div>
        <div class="insurance-estimated">
          <p>Deposit</p>
          <p class="estimated-price">{{ depositText }}</p>
        </div>
      </div>
      <button
        class="insurance-action active"
        @click="pay"
      >Pay {{ depositAmount | beautyCurrency }}
        <icon-arrow-right class="icon" size="16"></icon-arrow-right>
      </button>
      <div class="disclaimer" v-if="!isSameDeposit"><div class="disclaimer__content">Please note the current payment is not the total amount of the deposit.</div></div>
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
      :deposit-option="quoteDeposit"
      :deductible-option="quoteDeductible"
      :total="total"
      :monthly-payment="monthlyPayment"
      :deposit="deposit"
      :first-payment-due="firstPaymentDue"
      :deposit-payments="depositPayments"
      @close="setShowPremium(false)"
      ></modal-premium>
  </quote-process-columns-layout>
</template>

<script lang="ts">
import { Component, Vue, Watch, Prop } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class';

import { Route } from 'vue-router';

import { addDays, addMonths, format, differenceInDays } from 'date-fns';

import BasicButton from '@/components/buttons/basic-button.vue'
import DropdownInfo from '@/components/containers/dropdown-info.vue'
import IconArrowRight from '@/components/icons/icon-arrow-right.vue'
import IconInfo from '@/components/icons/icon-info.vue'
import InputDatepicker from '@/components/inputs/input-datepicker.vue'
import ModalPremium from '@/apps/quote/components/modals/modal-premium.vue'
import QuoteProcessColumnsLayout from '@/apps/quote/components/layout/quote-process-columns-layout.vue'
import QuoteSummary from '@/apps/quote/components/containers/quote-summary.vue'

import { RouteName } from '@/router'

import { QuoteProcess, QuoteProcessPayment } from '@/@types/quote';
import { User } from '@/@types/users';

import { currency, beautyCurrency } from '@/utils/text'
import { getHerefordFee, getPaymentsByDeposit } from '@/utils/quote'
import MonthlyPayment from '@/apps/quote/components/MonthlyPayment.vue'

const quote = namespace('Quote')
const quotePayment = namespace('QuotePayment')
const users = namespace('Users')

// Ninth Step 
@Component({
  components: {
    BasicButton, DropdownInfo, InputDatepicker, QuoteProcessColumnsLayout,
    IconArrowRight, IconInfo, QuoteSummary, ModalPremium, MonthlyPayment
  },
  filters: {
    currency, beautyCurrency
  }
})
export default class StepQuoteReview extends Vue {
  @quote.Getter
  quoteProcess?: QuoteProcess

  @quote.Getter
  quoteProcessId?: string

  @quotePayment.Getter
  quoteProcessPayment?: QuoteProcessPayment

  @users.Getter
  user?: User

  disabledDates = {
    to: new Date(),
    from: addDays(new Date(), 20)
  }

  showPremium = false;

  get hasDeductible(): boolean {
    return !!this.quoteProcess!.deductible;
  }

  get monthlyPayment(): number {
    return this.quoteProcessPayment!.monthly_payment;
  }

  get quoteDeductible(): number {
    return !!this.quoteProcess && !!this.quoteProcess.deductible ? this.quoteProcess.deductible:0
  }

  get isSameDeposit(): boolean {
    return this.deposit.toFixed(2) === this.depositPaymentAmount.toFixed(2)
  }

  get quoteDeposit(): number {
    return !!this.quoteProcess ? this.quoteProcess.deposit!:0
  }

  get quoteStartDate(): string {
    return !!this.quoteProcess ? this.quoteProcess.start_date!:''
  }

  get deposit(): number {
    return this.quoteProcessPayment!.deposit;
  }

  get herefordFee(): number {
    return this.quoteProcessPayment!.hereford_fee;
  }

  get depositText(): string {
    return this.quoteDeposit ? this.quoteDeposit == 100 ? beautyCurrency(this.prp) : beautyCurrency(this.deposit):'$--'
  }

  get depositPayments(): number {
    return getPaymentsByDeposit(this.quoteDeposit)
  }

  get depositPaymentAmount(): number {
    return !!this.quoteProcessPayment ? Number(this.quoteProcessPayment.deposit_payment_amount):0;
  }

  get depositAmount(): number {
    return !!this.quoteProcessPayment ? Number(this.quoteProcessPayment.deposit):0;
  }

  get firstPaymentDue(): string {
    if (!this.quoteStartDate) {
      return '--'
    }
    const selectedDate = new Date(this.quoteStartDate)
    // return this.formatDate(addMonths(selectedDate, this.depositPayments === 3 ? 9:3))
    return 'March 15, 2020'
  }

  get liability(): string {
    return !!this.quoteProcessPayment && !!this.quoteProcessPayment.liability_amount ? currency(Number(this.quoteProcessPayment.liability_amount)):''
  }

  get monthlyPaymentText(): string {
    return this.quoteDeposit ? beautyCurrency(this.monthlyPayment):'$--'
  }

  get physicalAmount(): number {
    return !!this.quoteProcessPayment!.physical_amount ? Number(this.quoteProcessPayment!.physical_amount):0
  }
  
  get total(): number {
    return !!this.quoteProcessPayment ? Number(this.quoteProcessPayment.official_hereford_quote):0
  }

  get prp(): number {
    const nodp = differenceInDays(new Date(this.quoteStartDate), new Date(2020, 2, 2));
    return this.total * (363 - nodp) / 363;
  }

  back(): void {
    this.$router.push({ name: RouteName.DASHBOARD })
  }

  formatDate(date: Date | string): string {
    return format(new Date(date), 'MMM d, yyyy')
  }

  async pay(): Promise<void> {
    this.$router.push({ name: RouteName.PAYMENT })
  }

  setShowPremium(value: boolean): void {
    this.showPremium = value;
  }
  async beforeRouteEnter (to: Route, from: Route, next: any): Promise<void> {
    next(async (vm: StepQuoteReview) => {
      if (!vm.user || !vm.quoteProcess || !vm.quoteProcessPayment || !!vm.quoteProcessPayment.payment_date) {
          // We want the user to came from the dashboard
          vm.$router.push({ name: RouteName.DASHBOARD })
        }
    })
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
  background-color: $white;
  border-radius: 8px;
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
  padding: 1.25rem 0.5rem;

  &.insurance-resume--single {
    justify-content: center;
    
    .insurance-estimated {
      width: 100%;
    }
  }

  .insurance-estimated {
    background-color: $white;
    border-radius: 2px;
    text-align: center;
    display: flex;
    flex-direction: column;
    padding: 1rem 0.875rem 0.875rem;
    width: 9.5rem;
    
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

        sup {
          font-size: $fs-sm;
          font-weight: $fw-semibold;
        }
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

  .questions__result {
    align-items: center;
    display: flex;
    justify-content: space-between;
    padding: 0.25rem 1.25rem;

    .questions__title {
      color:$blue-dark;
      font-size: $fs-lg;
      font-weight: $fw-bold;
      line-height: 1.22;
    }
  }
}

.disclaimer {
  background-color: $white;
  border: 1px solid $orange;
  border-radius: 4px;
  color: $blue-dark;
  margin-top: 1.5rem;
  line-height: 24px;

  .disclaimer__content {
    background-color: rgba(247, 103, 7, 0.08);
    border-radius: 4px;
    padding: 0.75rem 1.25rem;
  }

  span {
    font-weight: $fw-semibold;
  }
}

.monthly-payment-wrapper {
  background-color: $white;
  padding: 1rem 0.875rem 0.875rem;
  margin-right: 0.5rem;
}
</style>
