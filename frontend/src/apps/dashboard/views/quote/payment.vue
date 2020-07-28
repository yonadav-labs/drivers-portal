<template>
  <div class="docs-view" ref="main" v-if="!!quoteProcessPayment">
    <h3 class="title" v-if="!isPaymentDone">Your Official Hereford Quote is ready!</h3>
    <h3 class="title" v-else>Your payment has been received! {{ depositAmount < 0.01 ? `The deposit has been paid by ${thirdPartyName}.` : '' }}</h3>
    <div class="docs-header">
      <div class="docs-header__info">
        <p class="docs-header__explain" v-if="!isPaymentDone">Our team has reviewed the documents provided and your Official Hereford Quote is ready. 
          <br><span>The deposit amount due is <span class="docs-header__amount-due">{{ depositPaymentAmount | beautyCurrency }}</span>.</span>
          <br><span v-if="thirdPartyAmount"><span class="docs-header__amount-due">{{ thirdPartyAmount | beautyCurrency }}</span> from the deposit has been covered by <span class="docs-header__amount-due">{{ thirdPartyName }}</span>.</span>
        </p>
        <p class="docs-header__explain" v-else>Our team is preparing your new policy documents. You will be notified at {{ user.email }} when your policy is ready! 
        </p>
        <contained-button v-if="!isPaymentDone" class="docs-header__cta" color="blue" icon="dollar" @click="goToPayment">Procceed to Payment</contained-button>
      </div>
      <MonthlyPayment :qrsf="total" :deposit="depositPaymentAmount" :internalDeposit="depositPaymentPercentage" :internalDate="startDate" />

      <div class="docs-header__deposit" v-if="!!quoteProcessPayment & !isPaymentDone">
        <div class="estimate">
          <p>Deposit</p>
          <p class="estimate__price">{{ depositPaymentAmount|beautyCurrency }}</p>
          <span class="estimate__info">
            {{ depositPaymentPercentage }}% of total price
          </span>
        </div>
      </div>
      <div class="docs-header__total" v-if="!!quoteProcessPayment & !isPaymentDone">
        <div class="estimate">
          <p>Total</p>
          <p class="estimate__price">{{ prp|beautyCurrency }}</p>
          <span class="estimate__info">
            Insurance Premium
          </span>
        </div>
      </div>
    </div>
    <div class="docs-section" v-if="!!quoteProcessDocuments">
      <div class="info-message" v-if="!isPaymentDone && oldQuote != total">
        <div class="info-message__info">
          <div class="info-message__title">Why is my quote different?</div>
          <p class="info-message__explain">
            After reviewing the documentation, the Stable team found some differences between the data provided
            during the quote process and the documents provided. If you have additional questions, please, reach
            our team at <a class="info-message__link" href="mailto:support@stableins.com">support@stableins.com</a>
          </p>
        </div>
      </div>
      <div class="broker-section broker-section--submitted">
        <div class="broker-section__info">
          <div class="broker-section__title">Broker of Record Change</div>
        </div>
        <div class="broker-section__cta">
          <div class="broker-section__signed">Signed <i><icon-check-circle size="16"></icon-check-circle></i></div>
        </div>
      </div>
      <div class="documents documents--done">
        <div class="document-row" v-for="doc in filteredDocs" :key="doc.title">
          <div class="document-row__name">
            <span class="document-row__doc-title">{{ doc.title }}</span>
            <span class="document-row__filename" :title="getDocumentUrl(doc.field) | getFilename">{{ getDocumentUrl(doc.field) | getFilename }}</span>
          </div>
          <div class="document-row__actions">
            <contained-button color="grey" icon="file-download" @click="downloadDoc(getDocumentUrl(doc.field))">Download</contained-button>
          </div>
        </div>
        <div class="document-row document-row--has-children" v-if="!!accidentReports">
          <div class="document-row__name">
            Accident Reports
          </div>
          <div class="document-row__children">
            <div v-for="(report, index) in accidentReports" :key="report.id" class="document-row">
              <div class="document-row__name">
                Accident Report #{{ index + 1}} 
                <span class="document-row__filename" v-if="!!report.accident_report" :title="report.accident_report | getFilename">{{ report.accident_report | getFilename }}</span>
              </div>
              <div class="document-row__actions">
                <button-icon class="document-row__action-icon" :disabled="!report.accident_report" @click="downloadDoc(report.accident_report)"><icon-file-download></icon-file-download></button-icon>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class';

import { format, addMonths, differenceInDays } from 'date-fns';

import { DashboardQuoteRouteName } from '@/router/dashboard'
import { RouteName } from '@/router'

import { QuoteProcess, QuoteProcessDocuments, QuoteProcessDocumentsAccidentReport, QuoteProcessPayment } from '@/@types/quote';
import { User } from '@/@types/users';

import BasicButton from '@/components/buttons/basic-button.vue'
import ButtonIcon from '@/components/buttons/button-icon.vue'
import ContainedButton from '@/components/buttons/contained-button.vue'

import FileUploadHandler from '@/components/inputs/file-upload-handler.vue'

import IconCheckCircle from '@/components/icons/icon-check-circle.vue'
import IconFileDownload from '@/components/icons/icon-file-download.vue'

import { beautyCurrency, getFilename } from '@/utils/text'
import { getHerefordFee, getPaymentsByDeposit } from '@/utils/quote'
import MonthlyPayment from '@/apps/quote/components/MonthlyPayment.vue'

import { Route } from 'vue-router';

const quote = namespace('Quote')
const quoteDocs = namespace('QuoteDocuments')
const quotePayment = namespace('QuotePayment')
const users = namespace('Users')

interface DocElement {
  title: string,
  field: string,
  disabled: boolean
}

@Component({
  components: {
    BasicButton, ButtonIcon, ContainedButton, FileUploadHandler, IconCheckCircle, IconFileDownload, MonthlyPayment
  },
  filters: {
    beautyCurrency, getFilename
  }
})
export default class DashboardQuotePaymentView extends Vue {
  @quote.Getter
  quoteProcess?: QuoteProcess

  @quoteDocs.Getter
  quoteProcessDocuments?: QuoteProcessDocuments

  @quotePayment.Getter
  quoteProcessPayment?: QuoteProcessPayment

  @users.Getter
  user!: User

  @quoteDocs.Action
  retrieveQuoteProcessDocuments!: () => Promise<void>

  @quotePayment.Action
  retrieveQuoteProcessPayment!: () => Promise<void>


  docs: DocElement[] = [
    {
      title: 'DMV License Front Side',
      field: 'dmv_license_front_side',
      disabled: false
    },
    {
      title: 'DMV License Back Side',
      field: 'dmv_license_back_side',
      disabled: false
    },
    {
      title: 'TLC License Front Side',
      field: 'tlc_license_front_side',
      disabled: false
    },
    {
      title: 'TLC License Back Side',
      field: 'tlc_license_back_side',
      disabled: false
    },
    {
      title: 'Loss Run Document',
      field: 'loss_run',
      disabled: false
    },
    {
      title: 'Vehicle Title, Bill of Sale, or MV-50',
      field: 'vehicle_title',
      disabled: false
    },
    {
      title: 'Base Letter',
      field: 'base_letter',
      disabled: false
    },
    {
      title: 'Proof of Address',
      field: 'proof_of_address',
      disabled: false
    },
    {
      title: 'Defensive Driving Certificate',
      field: 'defensive_driving_certificate',
      disabled: false
    },
  ]

  get accidentReports(): QuoteProcessDocumentsAccidentReport[] {
    return !!this.quoteProcessDocuments ? this.quoteProcessDocuments.accident_reports:[];
  }

  get depositAmount(): number {
    return !!this.quoteProcessPayment ? this.quoteProcessPayment.deposit:0;
  }

  get depositPaymentAmount(): number {
    return !!this.quoteProcessPayment ? Number(this.quoteProcessPayment.deposit_payment_amount):0;
  }

  get filteredDocs(): DocElement[] {
    return this.docs.filter(
      doc => !!this.quoteProcessDocuments && !!this.quoteProcessDocuments[doc.field]
    )
  }

  get isPaymentDone(): boolean {
    return !!this.quoteProcessPayment && !!this.quoteProcessPayment.payment_date
  }

  get monthlyPayment(): number {
    return !!this.quoteProcessPayment ? this.quoteProcessPayment.monthly_payment:0;
  }

  get herefordFee(): number {
    return !!this.quoteProcessPayment ? this.quoteProcessPayment.hereford_fee:0;
  }

  get depositPayments(): number {
    return getPaymentsByDeposit(this.quoteDeposit)
  }

  get firstPaymentDue(): string {
    if (!this.startDate) {
      return '--'
    }
    const selectedDate = new Date(this.startDate)
    // return format(addMonths(selectedDate, this.depositPayments === 3 ? 9:3), 'MMM d, yyyy')
    return 'March 15, 2020'
  }

  get oldQuote(): number {
    return Number(this.quoteProcess!.quote_amount)
  }

  get startDate(): string {
    return (!!this.quoteProcess && this.quoteProcess.start_date) || ''
  }

  get quoteDeposit(): number {
    return (!!this.quoteProcess && this.quoteProcess.deposit !== undefined) ? this.quoteProcess.deposit:0;
  }

  get depositPaymentPercentage(): number {
    return !!this.quoteProcessPayment ? Number(this.quoteProcessPayment.deposit_percentage):0
  }

  get total(): number {
    return !!this.quoteProcessPayment ? Number(this.quoteProcessPayment.official_hereford_quote):0
  }

  get prp(): number {
    const nodp = differenceInDays(new Date(this.startDate), new Date(2020, 2, 2));
    return this.total * (363 - nodp) / 363;
  }

  get hasThirdPartyDeposit(): boolean {
    return !!this.quoteProcessPayment ? this.quoteProcessPayment.has_third_party_deposit:false
  }

  get thirdPartyName(): string {
    return !!this.quoteProcessPayment ? this.quoteProcessPayment.third_party_name:''
  }

  get thirdPartyAmount(): number {
    return !!this.quoteProcessPayment ? Number(this.quoteProcessPayment.third_party_amount):0
  }

  downloadDoc(url: string): void {
    const link = document.createElement('a');
    link.target = '_blank';
    link.download = getFilename(url);
    link.href = url;
    link.click();
  }

  getDocumentUrl(field: string): string {
    return this.quoteProcessDocuments![field]
  }
 
  goToPayment(): void {
    this.$router.push({ name: RouteName.REVIEW })
  }

  beforeRouteEnter (to: Route, from: Route, next: any): void {
    next(async (vm: DashboardQuotePaymentView) => {
      await vm.retrieveQuoteProcessDocuments()
      await vm.retrieveQuoteProcessPayment()
    })
  }
}
</script>

<style lang="scss" scoped>
.title {
  font-size: 1.25rem;
  line-height: 24px;
  font-weight: $fw-semibold;
}

.docs-header {
  display: flex;
  flex-flow: row nowrap;
  justify-content: space-between;
  margin-top: 0.75rem;

  .docs-header__info {
    flex-grow: 1;
  }

  .docs-header__explain {
    color: $grey-darker;
    line-height: 24px;

    .docs-header__amount-due {
      color: $blue-dark;
    }
  }

  .docs-header__cta {
    margin-top: 0.625rem;
  }
}

.estimate {
  background-color: $white;
  border-radius: 2px;
  text-align: center;
  display: flex;
  flex-direction: column;
  width: 9.813rem;

  span {
    font-size: $fs-lg;
  }
  p {
    text-align: center;
  
    &.estimate__price {
      color: $blue;
      font-size: 24px;
      font-weight: $fw-semibold;
      line-height: 20.43px;
      margin-top: 1rem;
      margin-bottom: 1rem;

      sup {
        font-size: $fs-sm;
        font-weight: $fw-semibold;
      }
    }
  }
  .estimate__info {
    background-color: $grey-light;
    font-size: $fs-xs;
    line-height: 14px;
    margin: 0 auto;
    opacity: 0.5;
    padding: 0.5rem;
  }
}

.status {
  background-color: rgba(206, 212, 218, 0.4);
  border-radius: 4px;
  color: $grey-darker;
  display: inline-block;	
  font-size: $fs-xs;	
  font-weight: $fw-semibold;	
  letter-spacing: 1px;	
  line-height: 14px;	
  padding: 0.25rem 0.5rem;
  text-transform: uppercase;

  &.success {
    background-color: rgba(0, 195, 50, 0.2); // #00C332
    color: #00C332;
  }
}

.docs-section {
  border: 1px solid $grey-medium-light;
  border-radius: 8px;
  margin-top: 2rem;
  padding: 1.25rem;
}

.broker-section {
  align-items: center;
  background-color: rgba(66,99,235,0.04);
  border: 1px solid $blue;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.875rem;
  padding: 1.25rem 1.875rem;

  .broker-section__info {
    padding-left: 0.625rem;

    .broker-section__title {
      align-items: center;
      color: $blue-dark;
      display: flex;
      font-weight: $fw-semibold;
      line-height: 24px;

      .status {
        margin-left: 0.75rem;
      }
    }

    .broker-section__explain {
      color: $grey-darker;
      line-height: 24px;
      margin-top: 0.25rem;
    }
  }

  .broker-section__cta {
    flex-shrink: 0;
    margin-left: 7rem;
    
    .broker-section__signed {
        align-items: center;
        background-color: $white;
        border-radius: 4px;
        display: inline-flex;
        color: $blue;
        font-weight: $fw-semibold;
        justify-content: center;
        padding: 0.875rem 0.7625rem;

        i {
          margin-left: 1.75rem;
        }
    }
  }

  &.broker-section--submitted {
    background-color: transparent;
    border: 1px solid $grey-medium-light;
    margin-bottom: 0.25rem;
    padding: 0.75rem 1.875rem;

    .broker-section__info {
      .broker-section__title {
        .status {
          display: none;
        }
      }

      .broker-section__explain {
        display: none;
      }
    }

  }
}

.documents {
  .documents__header {
    align-items: center;
    display: flex;	
    padding: 0.75rem 2.25rem;

    .documents__header-name {
      color: $grey-darker;
      font-size: $fs-xs;	
      font-weight: $fw-semibold;	
      letter-spacing: 1px;	
      line-height: 14px;	
      text-transform: uppercase;

      &.documents__header-name--document {
        flex-basis: 30%;
      }

      &.documents__header-name--status {
        flex-grow: 1;
      }

      &.documents__header-name--actions {
        flex-basis: 14.75rem;
      }
    }
  }

  .documents__add-accident {
    align-items: center;
    display: flex;
    justify-content: center;
    margin: 0.75rem 0 0.25rem;

    button {
      color: $grey-darker;
      margin: unset;
      font-size: 1rem;
      font-weight: $fw-semibold;
      line-height: 19px;
      
      .svg-icon-center {
        position: relative;
        top: -1px;
      }
    }
  }

  .document-row {
    align-items: center;
    border-radius: 4px;
    display: flex;
    flex-wrap: wrap;
    margin-top: 0.25rem;
    padding-bottom: 0.75rem;
    padding-top: 0.75rem;

    &:not(.document-row--has-children) {
      border: 1px solid $grey-medium-light;
    }

    &.document-row--has-children {
      background-color: $grey-opacity;
      padding-bottom: 1.25rem;
      padding-top: 1.25rem;
    }
  
    .document-row__status {
      flex-grow: 1;
    }

    .document-row__actions {
      align-items: center;
      display: flex;
      flex-basis: 14.75rem;
      justify-content: space-between;
      margin-right: 2.25rem;

      .document-row__action-icon {
        color: $grey;
      }
    }

    .document-row__name {
      display: flex;
      flex-basis: 30%;
      flex-flow: column nowrap;
      justify-content: flex-start;
      max-width: 30%;
      padding-left: 2.25rem;

      .document-row__doc-title {
        color: $blue-dark;
        font-weight: $fw-semibold;
        line-height: 24px;
        white-space: nowrap;
      }

      .document-row__filename {
        color: $grey-darker;
        max-width: calc(100% - 3rem);
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
    }

    .document-row__children {
      flex-basis: 100%;
      padding-left: 1.25rem;
      padding-right: 1.25rem;

      .document-row  {
        background-color: $white;
        border: 1px solid $grey-medium-dark;
        border-radius: 4px;
        justify-content: space-between;
        padding-left: 0;
        padding-right: 0;

        &:first-child {
          margin-top: 0.75rem;
        }

        .document-row__name {
          color: $blue-dark;
          flex-basis: calc(100% - 10rem);
          flex-flow: row nowrap;
          flex-grow: 1;
          font-weight: $fw-regular;
          line-height: 24px;
          max-width: calc(100% - 10rem);
          padding-left: calc(1.125rem);

          .document-row__filename {
            &::before {
              content: "—";
              margin-left: 0.5rem;
              margin-right: 0.5rem;
              position: relative;
            }
          }
        }

        .document-row__actions {
          flex-basis: 7rem;
          margin-right: 1.25rem;
        }
      }
    }
  }

  &.documents--done {

    .documents__header {
      display: none;
    }

    .document-row {
      .document-row__actions {
        justify-content: flex-end;
        flex-basis: 8rem;
        flex-grow: 1;
        margin-right: 1.875rem;
      }

      .document-row__status {
        display: none;
      }

      .status {
        display: none;
      }

      .document-row__name {
        align-items: center;
        flex-basis: calc(100% - 12.25rem);
        flex-flow: row nowrap;
        max-width: calc(100% - 12.25rem);
      }

      .document-row__filename {
        &::before {
          content: "—";
          margin-left: 0.5rem;
          margin-right: 0.5rem;
          position: relative;
        }
      }

      .document-row__children {
        .document-row__actions {
          .svg-icon-center {
            color: $blue !important;
          }
        }
      }
    }
  }
}

.info-message {
  align-items: center;
  background-color: rgba(66,99,235,0.04);
  border: 1px solid $blue;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.875rem;
  padding: 1.25rem 1.875rem;

  .info-message__info {
    padding-left: 0.625rem;

    .info-message__title {
      align-items: center;
      color: $blue-dark;
      display: flex;
      font-weight: $fw-semibold;
      line-height: 24px;
    }

    .info-message__explain {
      color: $grey-darker;
      line-height: 24px;
      margin-top: 0.25rem;
    }
  }

  .info-message__link {
    color: $blue;
    font-weight: $fw-semibold;
  }
}

.submit-review {
  display: flex;
  justify-content: flex-end;
  margin-top: 1.25rem;
}

.icon-report-upload {
  color: $grey-darker;
}
</style>
