<template>
  <div class="table">
    <div class="table-header">
      <div :class="{'ordering': orderby == 'payment'}" @click="setOrderBy('payment')">
        <span>
          <span>Payment</span>
          <icon-caret-up class="icon" size="12" v-if="orderby == 'payment' && asc == true"></icon-caret-up>
          <icon-caret-down class="icon" size="12" v-else></icon-caret-down>
        </span>
      </div>
      <div :class="{'ordering': orderby == 'dueDate'}" @click="setOrderBy('dueDate')">
        <span class="right">
          <span>Due Date</span>
          <icon-caret-up class="icon" size="12" v-if="orderby == 'dueDate' && asc == true"></icon-caret-up>
          <icon-caret-down class="icon" size="12" v-else></icon-caret-down>
        </span>
      </div>
      
      <div :class="{'ordering': orderby == 'payMade'}" @click="setOrderBy('payMade')">
        <span class="right">
          <span>Payment Made</span>
          <icon-caret-up class="icon" size="12" v-if="orderby == 'payMade' && asc == true"></icon-caret-up>
          <icon-caret-down class="icon" size="12" v-else></icon-caret-down>
        </span>
      </div>
      <div :class="{'ordering': orderby == 'amount'}" @click="setOrderBy('amount')">
        <span class="right">
          <span>Amount</span>
          <icon-caret-up class="icon" size="12" v-if="orderby == 'amount' && asc == true"></icon-caret-up>
          <icon-caret-down class="icon" size="12" v-else></icon-caret-down>
        </span>
      </div>
      <div :class="{'ordering': orderby == 'status'}" @click="setOrderBy('status')">
        <span>
          <span>Payment Status</span>
          <icon-caret-up class="icon" size="12" v-if="orderby == 'status' && asc == true"></icon-caret-up>
          <icon-caret-down class="icon" size="12" v-else></icon-caret-down>
        </span>
      </div>
    </div>
    <div v-for="(payment, index) in paymentsOrdered" :key="index" class="table-row">
      <span>{{payment.name}}</span>
      <span class="right">{{formatDate(payment.payment_due_date)}}</span>
      <span class="right">{{formatDate(payment.payment_date)}}</span>
        <span class="right">{{payment.payment_amount + payment.fee_amount | beautyCurrency}}</span>
        <span class="right status">
          <span>{{payment.status}}</span>
          <icon-circle class="icon--orange" size="8" :class="{'paid': payment.status === 'paid'}" ></icon-circle>
        </span>
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'

import { format, compareAsc } from 'date-fns';

import { PolicyPayment } from '@/@types/policy'

import IconCaretDown from '@/components/icons/icon-caret-down.vue'
import IconCaretUp from '@/components/icons/icon-caret-up.vue'
import IconCircle from '@/components/icons/icon-circle.vue'

import { beautyCurrency } from '@/utils/text'

@Component({
  components: { 
    IconCaretDown, IconCaretUp, IconCircle
  },
  filters: {
    beautyCurrency
  }
})
export default class StatusPaymentTable extends Vue {
  @Prop({ default: [] })
  payments!: PolicyPayment[]

  asc = false
  orderby: string | undefined = ''

  get paymentsOrdered(): PolicyPayment[] {
    return this.payments.sort((p1: PolicyPayment, p2: PolicyPayment) => {
      let res;
      switch(this.orderby) {
        case 'payment':
          res = p1.name.localeCompare(p2.name)
          break;
        case 'payMade':
          if (!!p1.payment_date && !!p2.payment_date) {
            res = compareAsc(p1.payment_date, p2.payment_date)
          } else {
            res = 1
          }
          break;
        case 'dueDate':
          res = compareAsc(p1.payment_due_date, p2.payment_due_date)
          break;
        case 'status':
          res = p1.status.localeCompare(p2.status)
          break;
        case 'amount':
          res = p1.payment_amount - p2.payment_amount
          break;
        default:
          res = 1
      }
      return this.asc ? res * -1 : res;
    })
  }

  setOrderBy(field:string):void {
    if (this.orderby === field) {
      this.asc = !this.asc;
    } else {
      this.asc = false;
      this.orderby = field;
    }
  }

  formatDate(date: Date): string {
    if (!!date) {
      return format(date, 'MM-dd-yyyy')
    } else {
      return '-'
    }
  }
}
</script>
<style lang="scss" scoped>
  .icon--orange{
    color: $orange;
    &.paid{
      color: $blue;
    }
  }
  .table {
    border-collapse: collapse;
    display: table;
    width: 100%;
    .right-check{
      display: flex;
      justify-content: flex-end;
      padding: 0.75rem 1.875rem;
    }
    .right.status{
      align-items: center;
      display: flex;
      justify-content: space-between;
      span {
        font-weight: $fw-regular;
      }
    }
    .table-header {
      display: table-row;
      & > div {
        cursor: pointer;
        display: table-cell;
        letter-spacing: 1px;
        padding: 12px 30px;
        text-transform: uppercase;
        .checkbox-text{
          color: $blue;
          margin-right: 0.75rem;
          line-height: 1.25rem;
        }
        span {
          align-items: stretch;
          color: $grey-darker;
          display: flex;
          font-size: $fs-xs;
          font-weight: bold;
          &.right {
            justify-content: flex-end;
          }
          .icon {
            margin-left: 10px;
          }
        }
        &.ordering {
          span {
            color: $blue-dark;
          }
        }
      }
    }
    .table-row {
      border: 1px solid rgba(206,212,218,0.4);
      border-bottom: 0;
      color: $blue-dark;
      cursor: default;
      display: table-row;
      &:last-child {
        border-bottom: 1px solid rgba(206,212,218,0.4);
      }
      &.selected {
        border: 1px solid $blue;
      }
      &.info {
        span {
          color:$grey-darker;
        }
      }
      & > span {
        display: table-cell;
        font-weight: $fw-regular;
        padding: 12px 30px;
        text-transform: capitalize;
        &.right {
          text-align: right;
        }
      }
    }
  }
</style>