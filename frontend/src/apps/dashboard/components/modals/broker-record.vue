<template>
  <modal @close="$emit('close')">
    <div class="modal-broker-record">
      <div class="modal-header">
        <span>Broker of Record Change</span>
        <div @click="$emit('close')" class="close">
          <icon-cross size="16"></icon-cross>
        </div>
      </div>
      <div class="modal-content">
        <h3>Please, read the following document carefully</h3>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. 
          Quod odio consectetur debitis dolor quas facere. Recusandae delectus veniam quod voluptate corporis beatae suscipit quisquam similique quo cum tempore, earum hic?
        </p>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. 
          Quod odio consectetur debitis dolor quas facere. Recusandae delectus veniam quod voluptate corporis beatae suscipit quisquam similique quo cum tempore, earum hic?
        </p>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. 
          Quod odio consectetur debitis dolor quas facere. Recusandae delectus veniam quod voluptate corporis beatae suscipit quisquam similique quo cum tempore, earum hic?
        </p>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. 
          Quod odio consectetur debitis dolor quas facere. Recusandae delectus veniam quod voluptate corporis beatae suscipit quisquam similique quo cum tempore, earum hic?
        </p>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. 
          Quod odio consectetur debitis dolor quas facere. Recusandae delectus veniam quod voluptate corporis beatae suscipit quisquam similique quo cum tempore, earum hic?
        </p>

        <checkbox
          class="checkbox"
          name="accept"
          :value="true"
          v-model="accepted"
        >
          <span>I have read the information above and accept the to change my broker.</span>
        </checkbox>
        <contained-button color="blue" :disabled="!accepted" @click="accept">Accept Broker Record Change</contained-button>
      </div>
    </div>
  </modal>
</template>

<script lang="ts">

import { Component, Vue, Prop, } from 'vue-property-decorator';

import Modal from '@/components/modals/modal.vue'

import ContainedButton from '@/components/buttons/contained-button.vue'
import Checkbox from '@/components/inputs/checkbox.vue'

import IconCross from '@/components/icons/icon-cross.vue'


import { Colors } from '@/utils/colors'

@Component({
  components: {
    Modal, ContainedButton, Checkbox, IconCross
  },
})
export default class ModalBrokerRecord extends Vue {
  accepted: boolean | string = '';

  accept() {
    this.$emit('submit')
  }
}
</script>

<style lang="scss" scoped>
.modal-broker-record {
  background-color: $white;
  border-radius: 8px;
  box-shadow: 0 10px 20px 0 rgba(206,212,218,0.4);
  max-width: 36.875rem;
  min-height: 33.25rem;
  padding: 0.625rem;
  width: calc(100vw - 8rem);
  z-index: 1;

  .modal-header {
    background-color: $blue;
    background-image: url("~@/assets/headerModal.png");
    background-repeat: no-repeat;
    background-size: cover;
    border-radius: 4px;
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
    padding: 1rem;
    max-height: calc(100vh - 1rem);
    overflow-y: auto;
  }
}

h3 {
  margin-bottom: 2rem;
}

p {
  margin-bottom: 1rem;
}

.checkbox {
  margin-bottom: 1.25rem;
  margin-top: 2rem;

  span {
    font-size: $fs-md;
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
</style>