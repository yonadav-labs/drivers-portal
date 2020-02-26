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
      <div class="selected">Policy documents</div>
    </div>
    <div class="documents-container">
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
  </div>
</div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class';

import { PolicyList, PolicyDetail } from '@/@types/policy';

import IconFileDownload from '@/components/icons/icon-file-download.vue'
import IconOpen from '@/components/icons/icon-open.vue'
import IconPdf from '@/components/icons/icon-pdf.vue'
import IconPrint from '@/components/icons/icon-print.vue'

import { getFilename } from '@/utils/text'
import { Route } from 'vue-router';
import { RouteName } from '@/router';

const policy = namespace('Policy')

interface DocElement {
  title: string,
  field: string,
}

@Component({
  components: {
    IconFileDownload, IconOpen, IconPdf, IconPrint
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

  get policy(): PolicyDetail | undefined {
    return this.policyById(this.policyId)
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
}
</script>

<style lang="scss" scoped>
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
  .policy-table--container{
    padding: 1.25rem 1.875rem;
  }
}
</style>