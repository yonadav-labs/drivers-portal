<template>
  <div class="policy-container" v-if="policy">
    <div class="policy-header">
      <h3 class="header-title">Policy #{{policy.policy_number }}</h3>
      <div class="header-content">
        <div class="header-group">
          <p>TLC #{{policy.tlc_number }}</p>
          <p>License Plate #{{policy.license_plate}}</p>
        </div>
        <div class="header-group">
          <p>VIN {{policy.vehicle_vin}}</p>
          <p></p>
        </div>
      </div>
    </div>
    <div class="policy-content">
      <div class="policy-menu">
        <div @click="() => policySection = 'documents'" :class="{'selected': policySection == 'documents'}">Policy documents</div>
        <div @click="() => policySection = 'payment'" :class="{'selected': policySection == 'payment'}">Payment</div>
      </div>
      <div v-if="policySection == 'documents'" class="documents-container">
        <p>Policy documents</p>
        <div class="list">
          <div class="item" v-for="(doc, index) in docs" :key="index">
            <div class="item-left">
              <icon-pdf size="16"></icon-pdf>
              <span class="item-title">{{doc.title}}</span>
            </div>
            <div class="item-right">
              <div class="item-icon" @click="open(doc.field)"><icon-open size="16"></icon-open></div>
              <div class="item-icon" @click="download(doc.field)"><icon-file-download size="16"></icon-file-download></div>
              <div class="item-icon" @click="print(doc.field)"><icon-print size="16"></icon-print></div>
            </div>
          </div>
        </div>
      </div>
      <div v-else-if="policySection == 'payment'" class="documents-container">
        <div class="policy-payment">
          <p class="policy-payment--title">Totals</p>
          <div class="policy-info">
            <div class="policy-info--content">
              <span class="policy-info--text">
                Total Premium
                <br>
                <span>{{+policy.premium | beautyCurrency}}</span>
              </span>
            </div>
            <div class="policy-info--content">
              <span class="policy-info--text">
                Amount Due
                <span>{{nextPaymentDue.payment_amount + nextPaymentDue.fee_amount | beautyCurrency}}</span>
              </span>
              <span class="policy-info--text">
                Next Payment Due
                <span>{{formatDate(nextPaymentDue.payment_due_date)}}</span>
              </span>
              <basic-button
                text='Make Payment'
                :color='colorWhite'
                :backgroundColor='colorBlue'
                class='button--rounded'
                @click="showPaymentModal = true"
              >
                <icon-dollar size='16' class='icon--white'></icon-dollar>
              </basic-button>
              <!-- <basic-button
                text='Auto Pay'
                :color='colorBlue'
                :backgroundColor='colorGreyMedium'
                class='button--rounded'
              >
                <icon-invoice-dollar size='16' class='icon--blue'></icon-invoice-dollar>
              </basic-button> -->
            </div>
          </div>
        </div>
        <div class="policy-table--container">
          <p class="policy-payment--title">Payment Information</p>
          <status-payment-table :payments="payments"></status-payment-table>
        </div>
      </div>
    </div>
    <modal-make-payment
      v-if="showPaymentModal"
      :payment="nextPaymentDue"
      @close="showPaymentModal = false"
      @success="paymentDone"
    ></modal-make-payment>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class';

import { PolicyList, PolicyDetail, PolicyPayment } from '@/@types/policy';

import { format, compareAsc, isAfter } from 'date-fns';

import BasicButton from '@/components/buttons/basic-button.vue'

import IconFileDownload from '@/components/icons/icon-file-download.vue'
import IconOpen from '@/components/icons/icon-open.vue'
import IconPdf from '@/components/icons/icon-pdf.vue'
import IconPrint from '@/components/icons/icon-print.vue'
import IconDollar from '@/components/icons/icon-dollar.vue'
import IconInvoiceDollar from '@/components/icons/icon-invoice-dollar.vue'

import StatusPaymentTable from '@/apps/dashboard/components/tables/status-payment-table.vue'
import ModalMakePayment from '@/apps/dashboard/components/modals/make-payment.vue'

import { beautyCurrency, getFilename } from '@/utils/text'
import { Colors } from '@/utils/colors'
import { Route } from 'vue-router';
import { RouteName } from '@/router';

const policy = namespace('Policy')

interface DocElement {
  title: string,
  field: string,
}

@Component({
  components: {
    IconFileDownload, IconOpen, IconPdf, IconPrint,
    IconDollar, IconInvoiceDollar, BasicButton,
    StatusPaymentTable, ModalMakePayment
  },
  filters: {
    beautyCurrency
  }
})
export default class DashboardPolicyView extends Vue {

  @policy.Getter
  policyList!: PolicyList[]

  @policy.Getter
  policyById!: (id: string) => PolicyDetail | undefined

  @policy.Action
  listPolicies!: () => Promise<void>

  @policy.Action
  retrievePolicyById!: (id: string) => Promise<void>

  docs: DocElement[] = [
    {
      title: 'Certificate of Liability',
      field: 'certificate_of_liability',
    },
    {
      title: 'FH1 Document',
      field: 'fh1_document',
    },
    {
      title: 'Insurance Document',
      field: 'insurance_document',
    }
  ]

  policyId = ''
  policySection = 'documents'
  showPaymentModal = false

  get policy(): PolicyDetail | undefined {
    return this.policyById(this.policyId)
  }

  get payments(): PolicyPayment[] {
    let index = 1
    return this.policy!.payments.map(
      (p: PolicyPayment) => {
        const payment_due_date = new Date(p.payment_due_date)
        const payment_date = p.payment_date ? new Date(p.payment_date) : undefined
        const status = p.is_paid ? 'paid' : isAfter(new Date(), payment_due_date) ? 'overdue' : 'pending'
        const payment_amount = +p.payment_amount
        const fee_amount = +p.fee_amount
        let name = 'Deposit'
        if (!p.is_deposit) {
          name = `Payment ${index}`
          index++
        }
        return {
          ...p,
          payment_due_date,
          payment_date,
          payment_amount,
          fee_amount,
          name,
          status
        }
      }
    )
  }

  get nextPaymentDue(): PolicyPayment | undefined {
    return this.payments.filter(
      (p: PolicyPayment) => p.is_paid === false
    ).sort(
      (p1: PolicyPayment, p2: PolicyPayment) => compareAsc(p1.payment_due_date, p2.payment_due_date)
    )[0]
  }

  get colorBlue(): string {
    return Colors.Blue
  }

  get colorWhite(): string {
    return Colors.White
  }

  get colorGreyMedium(): string {
    return Colors.GreyMedium
  }

  open(field: string): void {
    const url = this.policy![field]
    window.open(url, '_blank');
  }

  download(field: string): void {
    const url = this.policy![field]
    const link = document.createElement('a');
    link.href = url;
    link.download = `${getFilename(url)}`;
    link.dispatchEvent(new MouseEvent('click'));
  }

  print(field: string): void {
    const url = this.policy![field]
    const objFra = document.createElement('iframe');
    if (!!objFra) {
      objFra.style.visibility = 'hidden';
      objFra.src = url;
      document.body.appendChild(objFra);
      if (!!objFra.contentWindow) {
        objFra.contentWindow.focus();
        objFra.contentWindow.print();
      }
    }
  }

  paymentDone(): void {
    this.showPaymentModal = false
    this.retrievePolicyById(this.policyId)
  }

  async beforeRouteEnter(to: Route, from: Route, next: any): Promise<void> {
    next(async (vm: DashboardPolicyView) => {
      if (!vm.policyList.length) {
      await vm.listPolicies()
      }
      if (!!vm.policyList.length) {
        vm.policyId = vm.policyList[0].id;
        if (!vm.policy) {
          await vm.retrievePolicyById(vm.policyId)
        }
        if (!vm.policy) {
          this.$router.replace({ name: RouteName.DASHBOARD })
        }
      }
    })
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
.button--rounded {
  border-radius: 0.25rem;
  margin-left: 1rem;
  white-space: nowrap;
}

.policy-header {
  border-bottom: 1px solid rgba(206,212,218,0.4);
  padding: 1.25rem;

  .header-title {
    font-size: 20px;
    font-weight: $fw-semibold;
    margin-bottom: 1rem;
  }

  .header-content {
    display: flex;

    .header-group {
      min-width: 15.625rem;
      margin-right: 0.75rem;
      p {
        font-weight: $fw-regular;
      }
      p:last-child {
        color: $grey-darker;
        margin-top: 0.25rem;
      }
    }
  }
}

.documents-container {
  padding: 1.25rem;
  width: 100%;

  p {
    font-size: $fs-lg;
    font-weight: $fw-regular;
    margin: 0 0 0.25rem 1rem;
  }

  .list {
    align-items: stretch;
    display: flex;
    flex-direction: column;
    justify-content: center;

    .item {
      align-items: center;
      border: 1px solid #CED4DA;
      border-radius: 4px;
      color: $grey-darker;
      cursor: default;
      display: flex;
      justify-content: space-between;
      margin-top: 0.5rem;
      padding: 0.625rem 1.25rem;

      &:hover {
        background-color: rgba(206,212,218,0.2);
      }

      span{
        font-weight: $fw-regular;
      }
      
      .item-left {
        align-items: center;
        display: flex;
        flex: 1 1;

        .item-title {
          color: $blue-dark;
          margin-left: 1.875rem;
        }
      }

      .item-right {
        align-items: center;
        display: flex;
        justify-content: space-evenly;

        .item-icon {
          cursor: pointer;
          margin-left: 1.875rem;

          &:hover {
          color: $blue;
          }
        }
      }
    }
  }
}

.policy-container {
  border: 1px solid $blue;
  border-radius: 2px;
  box-shadow: 0 0.75rem 1.25rem 0 rgba(206,212,218,0.4);
  margin-bottom: 1.25rem;
  position: relative;
  width: 100%;
}

.policy-content {
  width: 100%;

  .policy-menu {
    border-bottom: 1px solid rgba(206,212,218,0.4);
    display: flex;
    margin: 0 10px;
    padding: 0 10px;
    width: calc(100% - 1.25rem);
    div {
      color: $blue;
      cursor: pointer;
      font-size: $fs-sm;
      font-weight: $fw-semibold;
      letter-spacing: 1.17px;
      padding: 1rem;
      text-transform: uppercase;

      &.selected {
      background-color: rgba($blue, 0.1);
      border-top: 2px solid $blue;
      color: $blue-dark;
      }
      &:hover{
      background-color: rgba($blue, 0.1);
      color: $blue-dark;
      }
    }
  }
  .policy-payment{
    background-color: rgba(66, 99, 235, 0.1);
    margin: 0 0.625rem;
    padding: 1.25rem;
    .policy-payment--title {
      margin-bottom: 0.5rem;
    }
    .policy-info{
      display: flex;
      .policy-info--content{
        align-items: center;
        background-color: $white;
        border-radius: 2px;
        display: flex;
        flex-grow: 1;
        padding:0.75rem 1.25rem;
        .pay-button.pay-button--white{
            margin-right: 0;
        }
        .policy-info--text{
          font-weight: $fw-regular;
          margin-right: 5rem;
          white-space: nowrap;
          span{
            color: $blue;
            font-size: 1.25rem;
            font-weight: $fw-semibold;
            display: block;
            line-height: 1.2;
            margin-top: 0.25rem;
            white-space: nowrap;
          }
        }
        &:first-child{
          margin-right: 2.5rem;
          flex-grow: 0;
          .policy-info--text{
            margin-right: 0;
          }
        }
      }
    }
  }
  .policy-table--container{
    padding: 1.25rem 1.875rem;
  }
}
</style>