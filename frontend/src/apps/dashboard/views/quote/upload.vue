<template>
  <div class="docs-view">
    <h3 class="title">Upload Documents</h3>
    <div class="docs-header">
      <div class="docs-header__info">
        <p class="docs-header__explain">In order to validate the quote we just showed you, please upload the documents below and our team will take care of the rest!
        </p>
        <contained-button class="docs-header__cta" color="blue" icon="check" :disabled="true">Submit for Review</contained-button>
      </div>
      <div class="docs-header__price">
        <div class="estimate">
          <p>Monthly price</p>
          <p class="estimate__price">{{ monthlyPayment|beautyCurrency }}</p>
          <span class="estimate__info">First Payment Due
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
    <div class="docs-section">
      <div class="broker-section">
        <div class="broker-section__info">
          <div class="broker-section__title">Broker of Record Change <div class="status">PENDING</div></div>
          <p class="broker-section__explain">
            Please review and sign our broker of record change so Stable can get you your insurance documents ASAP!
          </p>
        </div>
        <div class="broker-section__cta">
          <!-- <contained-button color="blue" icon="pen-alt">Sign now</contained-button> -->
          <div class="broker-section__signed">Signed <i><icon-check-circle size="16"></icon-check-circle></i></div>
        </div>
      </div>
      <div class="documents">
        <div class="documents__header">
          <div class="documents__header-name documents__header-name--document">Document</div>
          <div class="documents__header-name documents__header-name--status">Status</div>
          <div class="documents__header-name documents__header-name--actions">Actions</div>
        </div>
        <div class="document-row" v-for="doc in docs" :key="doc.title">
          <div class="document-row__name">
            {{ doc.title }}
          </div>
          <div class="document-row__status">
            <div class="status" :class="docFieldStatus(doc.field)">{{ docFieldStatusCopy(doc.field) }}</div>
          </div>
          <div class="document-row__actions">
            <button-icon class="document-row__action-icon" @click="downloadDoc(doc)" :disabled="!isDocUploaded(doc.field)"><icon-file-download></icon-file-download></button-icon>
            <button-icon class="document-row__action-icon" @click="removeDoc(doc)" :disabled="!isDocUploaded(doc.field)"><icon-trash-alt></icon-trash-alt></button-icon>
            <file-upload-handler @change="(file) => uploadDoc(doc, file)"><contained-button color="grey" icon="file-upload" :disabled="doc.disabled">Upload</contained-button></file-upload-handler>
          </div>
        </div>
        <div class="document-row document-row--has-children">
          <div class="document-row__name">
            Accident Reports
          </div>
          <div class="document-row__status">
            <div class="status">PENDING</div>
          </div>
          <div class="document-row__children">
            <div class="document-row">
              <div class="document-row__name">
                Accident Report #1
              </div>
              <div class="document-row__actions">
                <button-icon class="document-row__action-icon"><icon-file-download></icon-file-download></button-icon>
                <button-icon class="document-row__action-icon"><icon-trash-alt></icon-trash-alt></button-icon>
                <button-icon class="document-row__action-icon"><icon-file-upload></icon-file-upload></button-icon>
              </div>
            </div>
            <div class="documents__add-accident">
              <basic-button text="Add Accident Report"><icon-plus-circle slot="before"></icon-plus-circle></basic-button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="submit-review">
      <contained-button class="docs-header__cta" color="blue" icon="check" :disabled="true">Submit for Review</contained-button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class';

import { format, addMonths } from 'date-fns';

import { DashboardQuoteRouteName } from '@/router/dashboard'

import { QuoteProcess, QuoteProcessDocuments } from '@/@types/quote';

import BasicButton from '@/components/buttons/basic-button.vue'
import ButtonIcon from '@/components/buttons/button-icon.vue'
import ContainedButton from '@/components/buttons/contained-button.vue'

import FileUploadHandler from '@/components/inputs/file-upload-handler.vue'

import IconCheckCircle from '@/components/icons/icon-check-circle.vue'
import IconFileDownload from '@/components/icons/icon-file-download.vue'
import IconFileUpload from '@/components/icons/icon-file-upload.vue'
import IconPlusCircle from '@/components/icons/icon-plus-circle.vue'
import IconTrashAlt from '@/components/icons/icon-trash-alt.vue'

import { beautyCurrency, getFilename } from '@/utils/text'
import { Route } from 'vue-router';

const quote = namespace('Quote')
const quoteDocs = namespace('QuoteDocuments')

interface DocElement {
  title: string,
  field: string,
  disabled: boolean
}

@Component({
  components: {
    BasicButton, ButtonIcon, ContainedButton, FileUploadHandler, IconCheckCircle, IconFileDownload, IconFileUpload,
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

  @quoteDocs.Action
  retrieveQuoteProcessDocuments!: () => Promise<void>

  @quoteDocs.Action
  updateQuoteProcessDocumentsFile!: (payload: {field: string, file: File | ''}) => Promise<void>

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

  get depositAmount(): number {
    return this.quoteDeposit/100 * this.total
  }

  get monthlyPayment(): number {
    return (this.total * (1-(this.quoteDeposit/100)))/9;
  }

  get firstPaymentDue(): string {
    if (!this.startDate) {
      return '--'
    }
    const selectedDate = new Date(this.startDate)
    return format(addMonths(selectedDate, 3), 'MMM d, yyyy')
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

  docFieldStatus(field: string): string {
    return this.isDocUploaded(field) ? 'success':'pending'
  }

  docFieldStatusCopy(field: string): string {
    return this.isDocUploaded(field) ? 'uploaded':'pending'
  }

  downloadDoc(doc: DocElement): void {
    const link = document.createElement('a');
    link.target = '_blank';
    link.download = getFilename(this.quoteProcessDocuments[doc.field]);
    link.href = this.quoteProcessDocuments[doc.field];
    link.click();
  }

  isDocUploaded(field: string): boolean {
    return !!this.quoteProcessDocuments && !!this.quoteProcessDocuments[field]
  }

  async removeDoc(doc: DocElement): Promise<void> {
    await this.updateQuoteProcessDocumentsFile({field: doc.field, file: ''})
  }

  async uploadDoc(doc: DocElement, file: File): Promise<void> {
    doc.disabled = true;
    await this.updateQuoteProcessDocumentsFile({field: doc.field, file})
    doc.disabled = false;
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
}

.documents {
  .documents__header {
    align-items: center;
    display: flex;	
    margin-top: 1.875rem;
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
    padding: 0.75rem 0.75rem 0.25rem;

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
      color: $blue-dark;
      flex-basis: 30%;
      font-weight: $fw-semibold;
      line-height: 24px;
      padding-left: 2.25rem;
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
          flex-basis: unset;
          font-weight: $fw-regular;
          line-height: 24px;
          padding-left: calc(1.125rem);
        }

        .document-row__actions {
          flex-basis: 7rem;
          margin-right: 1.25rem;
        }
      }
    }
  }
}

.submit-review {
  display: flex;
  justify-content: flex-end;
  margin-right: 5rem;
  margin-top: 1.25rem;
}
</style>
