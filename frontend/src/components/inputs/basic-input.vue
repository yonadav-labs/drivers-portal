<docs>

</docs>

<template>
  <div class="container-input">
    <div class="box-input" :class="{'check':value!='' && !error,'wrong':error}">
      <input
        :type="type"
        :name="inputName"
        :placeholder="placeholder"
        :id="id"
        :required="required"
        :maxlength="maxlength"
        :value="value"
        :readonly="readonly"
        @input="input"
        @keyup="$emit('keyup')"
        @keyup.enter="$emit('keyupEnter')">
      <component
        v-bind:is="iconComponent"
        size="16"
        class="icon--grey"
        v-if="((!minlength && value =='') || (minlength && (!value || value.length < minlength)) || !validate)"
      ></component>
      <icon-check-circle size="16" class="icon--blue" v-else></icon-check-circle>
    </div>
    <p class="input-alert">
      <slot name="error"></slot>
    </p>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Model, Emit } from 'vue-property-decorator';

import IconIdCard from '@/components/icons/icon-id-card.vue'
import IconCheckCircle from '@/components/icons/icon-check-circle.vue'
import { VueConstructor } from 'vue';

@Component({
  components: {
    IconCheckCircle,
  }
})
export default class BasicInput extends Vue {

  @Prop()
  placeholder?: string;

  @Prop()
  id?: string;

  @Prop({ default: false })
  required?: boolean;

  @Prop({ default: false })
  readonly?: boolean;

  @Prop()
  inputName!: string;

  @Prop({ default: 'text' })
  type?: string;

  @Prop({ default: 'id-card' })
  icon?: 'id-card';
  
  @Prop()
  minlength?: number;

  @Prop()
  maxlength?: number;

  @Prop({ default: false })
  error?: boolean

  @Prop({ default: true })
  validate?: boolean

  @Prop()
  value!: string

  input(event: { target: HTMLInputElement; }): void {
    this.$emit('input', event.target.value);
  }

  get iconComponent(): VueConstructor<Vue> | undefined {
    switch (this.icon) {
      case 'id-card':
        return IconIdCard;
      default:
        return undefined;
    }
  }
}
</script>

<style lang="scss" scoped>
.icon--grey {
  color: $grey;
}
.icon--blue {
  color: $blue;
}
.container-input {
  .input-alert {
    font-size: $fs-md;
    margin-top: 0.25rem;
    text-align: left;
    line-height: 1.33;
    span {
      font-size: $fs-md;
      margin-top: 0.25rem;
      text-align: left;
      line-height: 1.33;
    }
  }
}
.box-input {
  align-items: center;
  background-color: $white;
  border: 1px solid $grey;
  border-radius: 2px;
  display: flex;
  margin-left: auto;
  margin-right: auto;
  justify-content: space-between;
  position: relative;
  padding: 0.5rem 1rem;
  &.wrong {
    animation: wrong-log 0.3s;
    border: 1px solid $orange;
  }
  &.check {
    border: 1px solid $blue;
    box-shadow: 0 0 3px 0 rgba(66, 99, 235, 0.5);
  }
  input {
    color: $blue-dark;
    font-size: $fs-lg;
    width: 85%;
    &::placeholder {
      color: $grey;
    }
    &:focus {
      outline: none;
    }
  }
}
@keyframes wrong-log {
  0% {
    left: 0px;
  }
  20% {
    left: 15px;
  }
  40% {
    left: -15px;
  }
  60% {
    left: 15px;
  }
  80% {
    left: -15px;
  }
  100% {
    left: 0px;
  }
}
</style>