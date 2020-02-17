<template>
  <div class="policy-container" v-if="policy">
  <div class="policy-header">
      <h3 class="header-title">{{policy.policy_number }}</h3>
      <div class="header-content">
    <div class="header-group">
          <p>{{policy.tlc_number }}</p>
          <p>{{policy.license_plate}}</p>
    </div>
    <div class="header-group">
          <p>{{policy.vehicle_vin}}</p>
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
              <icon-pdf size="20"></icon-pdf>
              <span class="item-title">{{doc.title}}</span>
      </div>
      <div class="item-right">
              <div class="item-icon" @click="open(doc.field)"><icon-open size="20"></icon-open></div>
              <div class="item-icon" @click="download(doc.field)"><icon-download size="20"></icon-download></div>
              <div class="item-icon" @click="print(doc.field)"><icon-print size="20"></icon-print></div>
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

import { getFilename } from '@/utils/text'
import { Route } from 'vue-router';

const policy = namespace('Policy')

interface DocElement {
  title: string,
  field: string,
}

@Component
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
    window.open(url, "_blank");
  }

  download(field: string): void {
    const url = this.policy![field]
    const link = document.createElement('a');
    link.href = url;
    link.download = `${getFilename(url)}.pdf`;
    link.dispatchEvent(new MouseEvent('click'));
  }

  print(field: string): void {
    const url = this.policy![field]
    const objFra = document.createElement('iframe');
    objFra.style.visibility = "hidden";
    objFra.src = url;
    document.body.appendChild(objFra);
    objFra.contentWindow.focus();
    objFra.contentWindow.print();
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
      }
  })
  }


}
</script>

<style lang="scss" scoped>
.policy-header {
  align-items: center;
  display: flex;
  justify-content: space-between;
  margin-bottom: 2.5rem;

  .documents-container {
    padding: 20px;
    width: 100%;

    p {
      font-size: $fs-lg;
      font-weight: $fw-regular;
      margin: 0 0 4px 16px;
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
          margin-top: 8px;
          padding: 10px 20px;

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
              margin-left: 30px;
            }

            .item-weight {
              color: $grey-darker;
              margin-left: 8px;
            }
          }

          .item-right {
            align-items: center;
            display: flex;
            flex: 1 1;
            justify-content: space-evenly;

            .item-icon {
              cursor: pointer;
              margin-left: 30px;

              &:hover {
                color: $blue;
              }
            }
          }
        }
      }
    }
  }
</style>