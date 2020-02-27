<template>
   <quote-process-layout v-if="!!quoteProcessPayment" :hide-breadcrumbs="true" :on-back="onBack" :hide-login="true" :simple-header="true">
    <div class="payment-info">
      <p class="form-explain">Deposit Payment</p>
      <p class="payment-info--price">{{ depositPaymentAmount|currency }}</p>
      <span class="payment-info--date" v-if="isSameDeposit">{{ quoteDeposit }}% of total price</span>
    </div>
    <div v-if="loading" class="spinner">
      Processing payment... Please, wait.
    </div>
    <div class="payment-error error-info" v-if="(hasError || fatalError || stripeError) && !loading">
      <p class="error-info--title">There was an error with your payment.</p>
      <p>{{ errorDisplay }}</p>
      <p v-if="stripeError">{{ !!stripeError.response ? stripeError.response.data[0]:stripeError.message }}</p>
      <p v-if="hasError && disabledBank && !fatalError">You can still pay with Credit Card</p>
    </div>

    <div class="form-container" v-if="!fatalError && !stripeError && !creditCardFormOpened && !loading">
      <p class="form-explain">How would you like to make the payment?</p>
      <form id="paymentForm">
        <div class="form-content form-content--pay">
          <pay-button text="Credit Card" :info="`${stripeFee} Fee`" @click.prevent="startPay()" color="#f76707">
            <!-- <icon-credit-card size="16" style="icon--orange"></icon-credit-card> -->
          </pay-button>
          <plaid-button
            v-if="!disabledBank"
            @success="plaidHandler"
            @exit="plaidExitHandler"
            :onClick="startPlaid">
            <template v-slot:button="props">
              <pay-button text="Bank" :info="`No Fee`" @click="props.onClick" color="#F76707">
                <!-- <icon-exchange size="16" style="icon--orange"></icon-exchange> -->
              </pay-button>
            </template>
          </plaid-button>
        </div>
      </form>
    </div>
    <credit-card-form
      v-show="!loading && !fatalError && !stripeError && creditCardFormOpened"
      :amount="depositPaymentAmount + stripeFeeAmount"
      @success="onCreditSuccess"
      @error="onCreditError"
      @loading="loading = true"
    ></credit-card-form>
   </quote-process-layout>
</template>


<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class'

import { Route } from 'vue-router';

import { QuoteProcess, QuoteProcessPayment } from '@/@types/quote';
import { StripeChargePayload, PlaidChargePayload } from '@/@types/payment';
import { User } from '@/@types/users';

import CreditCardForm from '@/components/forms/credit-card-form.vue'
import QuoteProcessLayout from '@/components/layout/quote-process-layout.vue'
import PayButton from '@/components/buttons/pay-button.vue'
import PlaidButton from '@/components/buttons/plaid-button.vue'

import { currency } from '@/utils/text'

import { DashboardQuoteRouteName } from '@/router/dashboard'
import { RouteName } from '@/router'

const quote = namespace('Quote')
const quotePayment = namespace('QuotePayment')
const users = namespace('Users')

@Component({
  components: {
    CreditCardForm, PayButton, PlaidButton, QuoteProcessLayout,
  },
  filters: {
    currency
  }
})
export default class DepositPaymentView extends Vue {
  @quote.Getter
  quoteProcess!: QuoteProcess

  @quote.Getter
  quoteProcessId?: string

  @quotePayment.Getter
  quoteProcessPayment!: QuoteProcessPayment

  @quotePayment.Getter
  stripeError?: Error | undefined

  @quotePayment.Getter
  plaidError?: Error | undefined

  @users.Getter
  user?: User

  @quotePayment.Action
  payDepositStripe!: (charge: StripeChargePayload) => void;

  @quotePayment.Action
  payDepositPlaid!: (charge: PlaidChargePayload) => void;

  @quotePayment.Action
  resetPayments!: () => void;

  disabledBank = false
  error = false
  fatalError = false;
  errorDisplay = ''
  loading = false
  creditCardFormOpened = false;

  get hasError(): boolean {
    return this.error || !!this.stripeError || !!this.plaidError
  }

  get quoteDeposit(): number {
    return !!this.quoteProcess ? this.quoteProcess.deposit!:0
  }

  get isSameDeposit(): boolean {
    return this.quoteDeposit.toFixed(2) === this.depositPaymentAmount.toFixed(2)
  }

  get depositAmount(): number {
    return this.quoteProcessPayment.deposit
  }

  get depositPaymentAmount(): number {
    return Number(this.quoteProcessPayment.deposit_payment_amount)
  }

  get stripeFeeAmount(): number {
   return this.quoteProcessPayment.stripe_fee 
  }

  get plaidFeeAmount(): number {
   return this.quoteProcessPayment.plaid_fee 
  }

  get stripeFee(): string {
    return currency(this.stripeFeeAmount)
  }

  get plaidFee(): string {
    return currency(this.plaidFeeAmount)
  }

  onBack(): void {
    if (this.creditCardFormOpened) {
      this.creditCardFormOpened = false;
    } else {
      this.$router.push({ name: RouteName.REVIEW })
    }
  }

  async plaidHandler({public_token, metadata}: {public_token: string, metadata: any}): Promise<void> {
    this.loading = true;
    await this.payDepositPlaid({
      public_token,
      account_id: metadata.account_id,
    })
    if (!this.plaidError) {
      this.$router.push({ name: DashboardQuoteRouteName.PAYMENT })
    } else {
      this.disabledBank = true;
    }
    this.loading = false;
  }

  plaidExitHandler({ result, err, metadata }: { result: string, err: any, metadata: any }): void {
    if (result==='plaid_error') {
      this.disabledBank = true;
      this.loading = false;
      this.error = true;
      this.errorDisplay = 'There was an error paying with Bank'
    }
  }

  startPlaid(): void {
    // pass
  }

  startPay(): void {
    this.creditCardFormOpened = true;
  }

  onCreditError(): void {
    this.error = true;
    this.fatalError = true;
    this.loading = false;
  }

  async onCreditSuccess(payload: StripeChargePayload): Promise<void> {
    await this.payDepositStripe(payload)
    if (!this.stripeError) {
      this.$router.push({ name: DashboardQuoteRouteName.PAYMENT })
    }
    this.loading = false;
  }

  async beforeRouteEnter (to: Route, from: Route, next: any): Promise<void> {
    next(async (vm: DepositPaymentView) => {
      if (!vm.user || !vm.quoteProcess || !vm.quoteProcessPayment || !!vm.quoteProcessPayment.payment_date) {
        vm.$router.push({ name: RouteName.DASHBOARD })
      }
      vm.resetPayments()
    })
  }

}
</script>


<style lang="scss" scoped>
.form-content--pay{
  display: flex;
  justify-content: center;
  margin-top: 1.25rem;
}

.payment-info {
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-top: 1.8rem;
  span {
    font-size: $fs-lg;
  }
  p {
    text-align: center;
    &.payment-info--price {
      color: $blue;
      font-size: $fs-xxl;
      font-weight: $fw-semibold;
      margin-top: 1rem;
      margin-bottom: 1rem;
    }
  }
  .payment-info--date {
    background-color: $grey-light;
    font-size: $fs-sm;
    margin: 0 auto;
    opacity: 0.5;
    padding: 0.5rem;
  }
}
.error-info {
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin: 1.875rem auto 1.25rem;
  width: 24rem;

  span {
    font-size: $fs-lg;
  }

  p {
    font-size: $fs-lg;
    line-height: 1.56;
    text-align: center;
    &.error-info--title {
      font-weight: $fw-bold;
    }
  }
}

.spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 22.5rem;
}

.or-separator {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}
</style>