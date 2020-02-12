<template>
   <quote-process-layout :hide-breadcrumbs="true" :hide-back="true" :hide-login="true" :simple-header="true">
    <div class="payment-info">
      <p class="form-explain">Deposit Payment</p>
      <p class="payment-info--price">$750</p>
      <span class="payment-info--date">25% of total price</span>
    </div>
    <div v-if="loading" class="spinner">
      <!-- <calculate-spinner :completedSteps="9" :total-steps="6"></calculate-spinner> -->
    </div>
    <div class="payment-error error-info" v-if="error && !loading">
      <p class="error-info--title">There was an error with your payment.</p>
      <p>{{ errorDisplay }}</p>
      <p v-if="error && disabledBank">You can still pay with Credit Card</p>
    </div>

    <div class="form-container" v-if="!openCreditCardForm && !loading">
      <p class="form-explain">How would you like to make the payment?</p>
      <form id="paymentForm">
        <div class="form-content form-content--pay">
          <pay-button text="Credit Card" info="$##.## Fee" @click.prevent="startPay()" color="#f76707">
            <icon-credit-card size="16" style="icon--orange"></icon-credit-card>
          </pay-button>
          <plaid-button
            :onSuccess="plaidHandler"
            :onExit="plaidExitHandler"
            :onClick="startPlaid">
            <template v-slot:button="props">
              <pay-button text="Bank" info="$##.## Fee" @click="props.onClick" color="#F76707">
                <icon-exchange size="16" style="icon--orange"></icon-exchange>
              </pay-button>
            </template>
          </plaid-button>
        </div>
      </form>
    </div>
    <credit-card-form
      v-if="openCreditCardForm"
      @resultCreditCardForm="onResultCreditCardForm"
    ></credit-card-form>
   </quote-process-layout>
</template>


<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class'
import { QuoteProcess, QuoteProcessPayment } from '@/@types/quote';

import CreditCardForm from '@/components/forms/credit-card-form.vue'
import QuoteProcessLayout from '@/components/layout/quote-process-layout.vue'
import PayButton from '@/components/buttons/pay-button.vue'
import PlaidButton from '@/components/buttons/plaid-button.vue'

const quote = namespace('Quote')
const quotePayment = namespace('QuotePayment')

@Component({
  components: {
    CreditCardForm, PayButton, PlaidButton, QuoteProcessLayout
  }
})
export default class DepositPayment extends Vue {
  @quote.Getter
  quoteProcess?: QuoteProcess

  @quotePayment.Getter
  quoteProcessPayment?: QuoteProcessPayment

  disabledBank = false
  error = false
  loading = false
  openCreditCardForm = false;

  plaidHandler(): void {
    // pass
  }
  plaidExitHandler(): void {
    // pass
  }
  startPlaid(): void {
    // pass
  }

  startPay(): void {
    this.openCreditCardForm = true;
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