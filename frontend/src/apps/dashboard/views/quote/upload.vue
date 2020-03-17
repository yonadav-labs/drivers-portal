<template>
  <div class="docs-view" ref="main">
    <h3 class="title">Upload Documents</h3>
    <div class="docs-header">
      <div class="docs-header__info">
        <p class="docs-header__explain">In order to validate the quote we just showed you, please upload the documents below and our team will take care of the rest!
        </p>
        <contained-button class="docs-header__cta" color="blue" icon="check" :disabled="!isReadyForSubmit" @click="submitForReview">{{ isSubmittedForReview ? 'Submitted for Review':'Submit for Review' }}</contained-button>
      </div>
      <div class="docs-header__price" v-if="monthlyPayment > 0">
        <div class="estimate">
          <p>Monthly price</p>
          <p class="estimate__price">{{ monthlyPayment|beautyCurrency }}<sup v-if="herefordFee">+{{ herefordFee | beautyCurrency }}</sup></p>
          <span class="estimate__info">{{ depositPayments }} payments starting on
            <br>
            {{ firstPaymentDue }}
          </span>
        </div>
      </div>
      <div class="docs-header__deposit">
        <div class="estimate">
          <p>Deposit</p>
          <p class="estimate__price">{{ depositAmount|beautyCurrency }}</p>
          <span class="estimate__info">
            {{ quoteDeposit }}% of total price
          </span>
        </div>
      </div>
      <div class="docs-header__total">
        <div class="estimate">
          <p>Total</p>
          <p class="estimate__price">{{ total|beautyCurrency }}</p>
          <span class="estimate__info">
            Insurance Premium
          </span>
        </div>
      </div>
    </div>
    <div class="docs-section" v-if="!!quoteProcessDocuments">
      <div class="success-message" v-if="isSubmittedForReview">
        <div class="success-message__info">
          <div class="success-message__title">Thank you for submitting all of your documents!</div>
          <p class="success-message__explain">
            Stable has kicked off the automated underwriting process. You will be notified in {{ user.email }} when your policy is ready! 
          </p>
        </div>
      </div>
      <div class="broker-section" v-if="quoteProcessDocuments.requires_broker_of_record" :class="{'broker-section--submitted': isSubmittedForReview}">
        <div class="broker-section__info">
          <div class="broker-section__title">Broker of Record Change <div class="status" :class="{'success': isBrokerOfRecordReady}">{{ isBrokerOfRecordReady ? 'SIGNED':'PENDING' }}</div></div>
          <p class="broker-section__explain">
            Please review and sign our broker of record change so Stable can get you your insurance documents ASAP!
          </p>
        </div>
        <div class="broker-section__cta">
          <div class="broker-section__signed" v-if="isValidatingSign && !isBrokerOfRecordReady">Validating...</div>
          <contained-button color="blue" icon="pen-alt" v-else-if="!quoteProcessDocuments.is_broker_of_record_signed" @click="openHelloSign">Sign now</contained-button>
          <div class="broker-section__signed" v-else>Signed <i><icon-check-circle size="16"></icon-check-circle></i></div>
        </div>
      </div>
      <div class="documents" :class="{'documents--disabled': !isBrokerOfRecordReady, 'documents--done': isSubmittedForReview}">
        <div class="documents__header">
          <div class="documents__header-name documents__header-name--document">Document</div>
          <div class="documents__header-name documents__header-name--status">Status</div>
          <div class="documents__header-name documents__header-name--actions">Actions</div>
        </div>
        <div class="document-row" v-for="doc in filteredDocs" :key="doc.title">
          <div class="document-row__name">
            <span class="document-row__doc-title">{{ doc.title }}</span>
            <span class="document-row__filename" v-if="isDocUploaded(doc.field)" :title="getDocumentUrl(doc.field) | getFilename">{{ getDocumentUrl(doc.field) | getFilename }}</span>
          </div>
          <div class="document-row__status">
            <div class="status" :class="docFieldStatus(doc.field)">{{ docFieldStatusCopy(doc.field) }}</div>
          </div>
          <div class="document-row__actions">
            <button-icon class="document-row__action-icon" @click="downloadDoc(getDocumentUrl(doc.field))" :disabled="!isDocUploaded(doc.field)" title="Download" v-if="!isSubmittedForReview"><icon-file-download></icon-file-download></button-icon>
            <button-icon class="document-row__action-icon" @click="removeDoc(doc)" :disabled="!isDocUploaded(doc.field)" title="Remove" v-if="!isSubmittedForReview"><icon-cross></icon-cross></button-icon>
            <file-upload-handler @change="(file) => uploadDoc(doc, file)" :disabled="!isBrokerOfRecordReady || doc.disabled" v-if="!isSubmittedForReview"><contained-button color="grey" icon="file-upload" :disabled="!isBrokerOfRecordReady || doc.disabled">Upload</contained-button></file-upload-handler>
            <contained-button color="grey" icon="file-download" @click="downloadDoc(getDocumentUrl(doc.field))" v-else>Download</contained-button>
          </div>
        </div>
        <div class="document-row document-row--has-children" v-if="minimumAccidentReports > 0">
          <div class="document-row__name">
            Accident Reports
          </div>
          <div class="document-row__status">
            <div class="status" :class="{'success': isAccidentReportsReady}">{{ isAccidentReportsReady ? 'UPLOADED':'PENDING' }}</div>
          </div>
          <div class="document-row__children">
            <div v-for="(report, index) in accidentReports" :key="report.id" class="document-row">
              <div class="document-row__name">
                Accident Report #{{ index + 1}} 
                <span class="document-row__filename" v-if="!!report.accident_report" :title="report.accident_report | getFilename">{{ report.accident_report | getFilename }}</span>
              </div>
              <div class="document-row__actions">
                <button-icon class="document-row__action-icon" :disabled="!report.accident_report" @click="downloadDoc(report.accident_report)"><icon-file-download></icon-file-download></button-icon>
                <button-icon class="document-row__action-icon" :disabled="!report.accident_report" v-if="!isSubmittedForReview && index < minimumAccidentReports" @click="createOrUpdateReport(report, '')"><icon-cross></icon-cross></button-icon>
                <button-icon class="document-row__action-icon" :disabled="!report.accident_report" v-else-if="!isSubmittedForReview" @click="deleteQuoteProcessDocumentsAccidentReport(report.id)"><icon-trash-alt></icon-trash-alt></button-icon>
                <file-upload-handler @change="(file) => createOrUpdateReport(report, file)" :disabled="!isBrokerOfRecordReady || report.disabled" v-if="!isSubmittedForReview"><button-icon class="document-row__action-icon" :disabled="!isBrokerOfRecordReady || report.disabled"><icon-file-upload class="icon-report-upload"></icon-file-upload></button-icon></file-upload-handler>
              </div>
            </div>
            <div class="documents__add-accident">
              <file-upload-handler @change="createQuoteProcessDocumentsAccidentReport" :disabled="!isAccidentReportsReady" v-if="!isSubmittedForReview"><basic-button text="Add Accident Report" :disabled="!isAccidentReportsReady"><icon-plus-circle slot="before"></icon-plus-circle></basic-button></file-upload-handler>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="submit-review">
      <contained-button v-if="!isSubmittedForReview" class="docs-header__cta" color="blue" icon="check" :disabled="!isReadyForSubmit" @click="submitForReview">Submit for Review</contained-button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class';

import { format, addMonths } from 'date-fns';

import HelloSign from 'hellosign-embedded';

import { DashboardQuoteRouteName } from '@/router/dashboard'

import { QuoteProcess, QuoteProcessDocuments, QuoteProcessDocumentsAccidentReport } from '@/@types/quote';
import { User } from '@/@types/users';

import BasicButton from '@/components/buttons/basic-button.vue'
import ButtonIcon from '@/components/buttons/button-icon.vue'
import ContainedButton from '@/components/buttons/contained-button.vue'

import FileUploadHandler from '@/components/inputs/file-upload-handler.vue'

import IconCheckCircle from '@/components/icons/icon-check-circle.vue'
import IconCross from '@/components/icons/icon-cross.vue'
import IconFileDownload from '@/components/icons/icon-file-download.vue'
import IconFileUpload from '@/components/icons/icon-file-upload.vue'
import IconPlusCircle from '@/components/icons/icon-plus-circle.vue'
import IconTrashAlt from '@/components/icons/icon-trash-alt.vue'

import { beautyCurrency, getFilename } from '@/utils/text'
import { getHerefordFee, getPaymentsByDeposit } from '@/utils/quote'

import { Route } from 'vue-router';

const quote = namespace('Quote')
const quoteDocs = namespace('QuoteDocuments')
const users = namespace('Users')

interface DocElement {
  title: string,
  field: string,
  disabled: boolean,
  non_hereford_only?: boolean
}

type QuoteProcessDocumentsAccidentReportElm = QuoteProcessDocumentsAccidentReport & { disabled: boolean }
type CreatedQuoteProcessDocumentAccidentReport = Omit<QuoteProcessDocumentsAccidentReportElm, 'id'>


@Component({
  components: {
    BasicButton, ButtonIcon, ContainedButton, FileUploadHandler, IconCheckCircle, IconCross, IconFileDownload, IconFileUpload,
    IconPlusCircle, IconTrashAlt
  },
  filters: {
    beautyCurrency, getFilename
  }
})
export default class DashboardQuoteUploadView extends Vue {
  @quote.Getter
  quoteProcess?: QuoteProcess

  @quoteDocs.Getter
  quoteProcessDocuments?: QuoteProcessDocuments

  @users.Getter
  user!: User
  
  @quoteDocs.Action
  createQuoteProcessDocumentsAccidentReport!: (file: File) => Promise<void>

  @quoteDocs.Action
  deleteQuoteProcessDocumentsAccidentReport!: (id: string) => Promise<void>

  @quoteDocs.Action
  retrieveQuoteProcessDocuments!: () => Promise<void>

  @quoteDocs.Action
  updateQuoteProcessDocumentsFile!: (payload: {field: string, file: File | ''}) => Promise<void>

  @quoteDocs.Action
  updateQuoteProcessDocuments!: (payload: {is_broker_of_record_signed?: boolean, is_submitted_for_review?: boolean}) => Promise<void>

  @quoteDocs.Action
  updateQuoteProcessDocumentsAccidentReport!: (payload: {id: string, file: File | ''}) => Promise<void>


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
      disabled: false,
      non_hereford_only: true
    },
    {
      title: 'Vehicle Title, Bill of Sale, or MV-50',
      field: 'vehicle_title',
      disabled: false,
      non_hereford_only: true
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

  isValidatingSign = false
  intervalValidate: number | undefined = undefined

  get accidentReports(): Array<(CreatedQuoteProcessDocumentAccidentReport |QuoteProcessDocumentsAccidentReportElm) | { disabled: boolean }> {
    return (this.quoteAccidentReports as Array<CreatedQuoteProcessDocumentAccidentReport | QuoteProcessDocumentsAccidentReportElm>).concat(this.extraAccidentReports)
  }

  get filteredDocs(): DocElement[] {
    return this.docs.filter(
      doc => !doc.non_hereford_only || !this.quoteProcess!.is_hereford
    )
  }

  get isAccidentReportsReady(): boolean {
    return this.extraAccidentReports.length === 0 && this.quoteAccidentReports.slice(0, this.minimumAccidentReports).every(report => !!report.accident_report)
  } 

  get isBrokerOfRecordReady(): boolean {
    return !!this.quoteProcessDocuments && (!this.quoteProcessDocuments.requires_broker_of_record || this.quoteProcessDocuments.is_broker_of_record_signed)
  }

  get extraAccidentReports(): CreatedQuoteProcessDocumentAccidentReport[] {
    const extraDocs = this.minimumAccidentReports - this.quoteAccidentReports.length
    return extraDocs > 0 ? ([...Array(extraDocs)].map(
      _ => ({
        accident_report: '',
        disabled: false
      })
    )):[]
  }

  get quoteAccidentReports(): QuoteProcessDocumentsAccidentReportElm[] {
    return !!this.quoteProcessDocuments ? this.quoteProcessDocuments.accident_reports.map(r => ({...r, disabled: false})):[];
  }

  get minimumAccidentReports(): number {
    if (!!this.quoteProcess) {
      const accidents = parseInt(this.quoteProcess.fault_accidents_last_months, 0)
      if (!isNaN(accidents)) {
        return accidents
      }
    }
    return 0
  }

  get requiredDocsReady(): boolean {
    let valid = this.docs.slice(0, 4).every(
      doc => !!this.quoteProcessDocuments![doc.field]
    )
    if (valid && !this.quoteProcess!.is_hereford) {
      valid = !!this.quoteProcessDocuments!.loss_run && !!this.quoteProcessDocuments!.vehicle_title
    }
    return valid
  }

  get depositAmount(): number {
    return this.quoteDeposit/100 * this.total
  }

  get monthlyPayment(): number {
    const months = getPaymentsByDeposit(this.quoteDeposit)
    return (this.total * (1-(this.quoteDeposit/100)))/this.depositPayments;
  }

  get herefordFee(): number {
    return !!this.quoteDeposit ? getHerefordFee(this.quoteDeposit):0;
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

  get startDate(): string {
    return (!!this.quoteProcess && this.quoteProcess.start_date) || ''
  }

  get quoteDeposit(): number {
    return (!!this.quoteProcess && this.quoteProcess.deposit !== undefined) ? this.quoteProcess.deposit:0;
  }

  get total(): number {
    return !!this.quoteProcess ? Number(this.quoteProcess.quote_amount):0
  }

  get isReadyForSubmit(): boolean {
    return !!this.quoteProcessDocuments && !this.quoteProcessDocuments.is_submitted_for_review &&
    this.isBrokerOfRecordReady && this.isAccidentReportsReady && this.requiredDocsReady
  }

  get isSubmittedForReview(): boolean {
    return !!this.quoteProcessDocuments && this.quoteProcessDocuments.is_submitted_for_review
  }

  docFieldStatus(field: string): string {
    return this.isDocUploaded(field) ? 'success':'pending'
  }

  docFieldStatusCopy(field: string): string {
    return this.isDocUploaded(field) ? 'uploaded':'pending'
  }

  downloadDoc(url: string): void {
    const link = document.createElement('a');
    link.target = '_blank';
    link.download = getFilename(url);
    link.href = url;
    link.click();
  }

  isDocUploaded(field: string): boolean {
    return !!this.quoteProcessDocuments && !!this.quoteProcessDocuments[field]
  }

  getDocumentUrl(field: string): string {
    return this.isDocUploaded(field) ? this.quoteProcessDocuments![field]:''
  }

  async removeDoc(doc: DocElement): Promise<void> {
    await this.updateQuoteProcessDocumentsFile({field: doc.field, file: ''})
  }

  async uploadDoc(doc: DocElement, file: File): Promise<void> {
    doc.disabled = true;
    await this.updateQuoteProcessDocumentsFile({field: doc.field, file})
    doc.disabled = false;
  }

  async createOrUpdateReport(report: QuoteProcessDocumentsAccidentReportElm, file: File | ''): Promise<void> {
    report.disabled = true;
    if (!!report.id) {
      await this.updateQuoteProcessDocumentsAccidentReport({ id: report.id, file })
    } else if (file instanceof File) {
      await this.createQuoteProcessDocumentsAccidentReport(file);
    }
    report.disabled = false;
  }

  submitForReview(): void {
    if (this.isReadyForSubmit) {
      this.updateQuoteProcessDocuments({is_submitted_for_review: true});
    }
    window.scroll({
      top: 0,  
      behavior: 'smooth'
    });
  }

  validateSign(): void {
    if (this.quoteProcessDocuments) {
      this.isValidatingSign = !this.quoteProcessDocuments.is_broker_of_record_signed
      if (!this.isValidatingSign) {
        clearInterval(this.intervalValidate)
      }
    }
    this.retrieveQuoteProcessDocuments()
  }

  openHelloSign(): void {
    if (this.quoteProcessDocuments) {
      // @ts-ignore
      const client = new HelloSign({
        clientId: this.quoteProcessDocuments.hsr_client_id
      })
      
      client.open(this.quoteProcessDocuments.hsr_sign_url, {
        testMode: this.quoteProcessDocuments.hsr_test_mode || true
      })
      
      client.on('sign', () => {
        this.isValidatingSign = true
        this.intervalValidate = setInterval(
          () => this.validateSign(),
          5000
        )
      })

      client.on('close', this.retrieveQuoteProcessDocuments)
      
      client.on('cancel', this.retrieveQuoteProcessDocuments)
    }
  } 

  beforeRouteEnter (to: Route, from: Route, next: any): void {
    next((vm: DashboardQuoteUploadView) => {
      vm.retrieveQuoteProcessDocuments()
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

  .docs-header__explain {
    color: $grey-darker;
    line-height: 24px;
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

  &.documents--disabled {
    .document-row {
      background-color: $grey-opacity;
      border: none;

      &.document-row--has-children {
        .document-row__children {
          .document-row {
            background-color: transparent;
          }
        }

      }

      .document-row__actions {
        > :not(.file-upload-handler) {
          .svg-icon-center {
            color: $grey !important;
          }
        }
      }
    }

    .documents__add-accident {
      background-color: rgba(206, 212, 218, 0.4);
      border-radius: 4px;
      
      button {
        span {
          color: $grey-darker !important;  
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

.success-message {
  align-items: center;
  background-color: rgba(66,99,235,0.04);
  border: 1px solid $blue;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.875rem;
  padding: 1.25rem 1.875rem;

  .success-message__info {
    padding-left: 0.625rem;

    .success-message__title {
      align-items: center;
      color: $blue-dark;
      display: flex;
      font-weight: $fw-semibold;
      line-height: 24px;
    }

    .success-message__explain {
      color: $grey-darker;
      line-height: 24px;
      margin-top: 0.25rem;
    }
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
