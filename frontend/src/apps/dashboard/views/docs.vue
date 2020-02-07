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
          <p class="estimate__price">$760</p>
          <span class="estimate__info">First Payment Due
            <br>
            Oct. 7, 2019
          </span>
        </div>
      </div>
      <div class="docs-header__deposit">
        <div class="estimate">
          <p>Deposit</p>
          <p class="estimate__price">$125</p>
          <span class="estimate__info">
            20% of total price
          </span>
        </div>
      </div>
      <div class="docs-header__total">
        <div class="estimate">
          <p>Total</p>
          <p class="estimate__price">$4500</p>
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
            <div class="status">PENDING</div>
          </div>
          <div class="document-row__actions">
            <button-icon class="document-row__action-icon"><icon-file-download></icon-file-download></button-icon>
            <button-icon class="document-row__action-icon"><icon-trash-alt></icon-trash-alt></button-icon>
            <contained-button color="grey" icon="file-upload">Upload</contained-button>
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

import { DashboardRouteName } from '@/router/dashboard'

import BasicButton from '@/components/buttons/basic-button.vue'
import ButtonIcon from '@/components/buttons/button-icon.vue'
import ContainedButton from '@/components/buttons/contained-button.vue'
import IconCheckCircle from '@/components/icons/icon-check-circle.vue'
import IconFileDownload from '@/components/icons/icon-file-download.vue'
import IconFileUpload from '@/components/icons/icon-file-upload.vue'
import IconPlusCircle from '@/components/icons/icon-plus-circle.vue'
import IconTrashAlt from '@/components/icons/icon-trash-alt.vue'

@Component({
  components: {
    BasicButton, ButtonIcon, ContainedButton, IconCheckCircle, IconFileDownload, IconFileUpload,
    IconPlusCircle, IconTrashAlt
  }
})
export default class DashboardDocsView extends Vue {
  docs = [
    {
      'title': 'DMV License'
    },
    {
      'title': 'TLC License'
    },
    {
      'title': 'Proof of Address'
    },
    {
      'title': 'Defensive Driving Certificate'
    },
  ]
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
