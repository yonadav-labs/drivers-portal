<template>
  <modal @close="$emit('close')">
    <div class="modal-premium">
      <div class="modal-header">
        <span>Annualized premium info</span>
        <div @click="$emit('close')" class="close">
          <icon-cross size="16"></icon-cross>
        </div>
      </div>
      <div class="modal-content">
        <div class="total-amount">
          {{ total | currency }}
        </div>
      </div>
      <div class="total-desc">
        <p>This price is what you would have paid this year had your</p>
        <p>policy started on March 1, 2020. All of our</p>
        <p>policies renew on March 1 each year.</p>          
      </div>
    </div>
  </modal>
</template>

<script lang="ts">

import { Component, Vue, Prop, } from 'vue-property-decorator';

import Modal from '@/components/modals/modal.vue'
import IconCross from '@/components/icons/icon-cross.vue'
import IconChevronUp from '@/components/icons/icon-chevron-up.vue';
import IconChevronDown from '@/components/icons/icon-chevron-down.vue';

import { QuoteProcessCalcVariations, QuoteProcessVariationPhysical } from '@/@types/quote';

import { currency, beautyCurrency } from '@/utils/text'
import { getHerefordFee, getPaymentsByDeposit } from '@/utils/quote'

@Component({
  components: {
    Modal, IconCross, IconChevronUp, IconChevronDown
  },
  filters: {
    currency,
    beautyCurrency
  }
})
export default class ModalPremium extends Vue {
  @Prop({ default: 0 })
  total!: number;
}
</script>

<style lang="scss" scoped>
.modal-premium {
  background-color: $white;
  border: 1px solid $blue;
  border-radius: 4px;
  box-shadow: 0 10px 20px 0 rgba(206,212,218,0.4);
  max-width: 37.5rem;
  min-height: 27.25rem;
  width: calc(100vw - 8rem);
  z-index: 1;

  .modal-header {
    background-color: $blue;
    background-image: url("~@/assets/headerModal.png");
    background-repeat: no-repeat;
    background-size: cover;
    border-radius: 4px 4px 0 0;
    color: $white;
    padding: 1rem;
    text-align: center;

    span {
      color: $white;
      font-size: $fs-lg;
      font-weight: $fw-semibold;
    }
  }
  .modal-content {
    max-height: calc(100vh - 4rem);
    overflow-y: auto;
    padding: 1.5rem 4.5rem;
  }
  .total-amount {
    text-align: center;
    font-size: 57px;
    color: #4263eb;
    font-weight: 600;
    margin: 67px 0 36px 0;
  }
  .total-desc {
    text-align: center;
    margin: auto;
    font-size: 18px;

    p {
      margin-top: 8px;
    }
  }
  .close {
    cursor: pointer;
    float: right;
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    transform-origin: center center;
    &:hover {
      -webkit-transform: scale3d(1.2, 1.2, 1.2);
      transform: scale3d(1.2);
    }
  }
}
</style>