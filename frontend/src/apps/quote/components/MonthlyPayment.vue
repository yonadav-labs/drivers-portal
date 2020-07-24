<template>
  <div class="montly-estimated" v-if="!afterAugust">
    <h3>Monthly payment</h3>

    <div class="month-record">
      <span>August 4</span>
      <span class="estimated-price">{{ monthlyPaymentText | beautyCurrency }}+{{ herefordFee | beautyCurrency }}</span>
    </div>
    <div class="month-record">
      <span>August XX</span>
      <span class="estimated-price">{{ monthlyPaymentText | beautyCurrency }}+{{ herefordFee | beautyCurrency }}</span>
    </div>
    <div class="month-record">
      <span>September XX</span>
      <span class="estimated-price">{{ monthlyPaymentText | beautyCurrency }}+{{ herefordFee | beautyCurrency }}</span>
    </div>
    <div class="month-record">
      <span>Octorber XX</span>
      <span class="estimated-price">{{ monthlyPaymentText | beautyCurrency }}+{{ herefordFee | beautyCurrency }}</span>
    </div>
    <div class="month-record">
      <span>November XX</span>
      <span class="estimated-price">{{ monthlyPaymentText | beautyCurrency }}+{{ herefordFee | beautyCurrency }}</span>
    </div>

    <span class="estimated-date">The additional charge on each monthly payment is an installment fee charged by Hereford
    </span>
  </div>
  <div class="montly-estimated" v-else>
    <h3>Monthly payment</h3>

    <div class="month-record">
      <span>September 4</span>
      <span class="estimated-price">{{ monthlyPaymentText | beautyCurrency }}+{{ herefordFee | beautyCurrency }}</span>
    </div>
    <div class="month-record">
      <span>September XX</span>
      <span class="estimated-price">{{ monthlyPaymentText | beautyCurrency }}+{{ herefordFee | beautyCurrency }}</span>
    </div>
    <div class="month-record">
      <span>Octorber XX</span>
      <span class="estimated-price">{{ monthlyPaymentText | beautyCurrency }}+{{ herefordFee | beautyCurrency }}</span>
    </div>
    <div class="month-record">
      <span>November XX</span>
      <span class="estimated-price">{{ monthlyPaymentText | beautyCurrency }}+{{ herefordFee | beautyCurrency }}</span>
    </div>

    <span class="estimated-date">The additional charge on each monthly payment is an installment fee charged by Hereford
    </span>
  </div>
</template>

<script>
  import { currency, beautyCurrency } from '@/utils/text'
  export default {
    props: {
      monthlyPaymentText: Number,
      internalDate: [Date, String]
    },
    data() {
      return {
        monthlyPayment: 5,
        herefordFee: 67,
      }
    },
    computed: {
      afterAugust() {
        return new Date(this.internalDate) > new Date(2020, 6, 30);
      }
    },
    filters: {
      beautyCurrency
    }
  }
</script>

<style lang='scss' scoped>
h3 {
  margin-bottom: 0.7rem;
}
.month-record {
  color: $blue;
  margin-top: 0.3rem;
  span {
    display: inline-block;
    width: 50%;

    &:first-child {
      text-align: center;
      font-size: 1rem;
    }

    &:last-child {
      text-align: left;
      font-weight: 600;
    }
  }
}
.montly-estimated {
  background-color: $white;
  border-radius: 2px;
  text-align: center;
  display: flex;
  flex-direction: column;
  padding: 1rem 0.875rem 0.875rem;
  flex: 1;
  margin-right: 0.5rem;

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
    margin: 10px auto 0;
    opacity: 0.5;
    padding: 0.5rem;
  }
}
</style>