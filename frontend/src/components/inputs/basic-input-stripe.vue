<template>
  <div class="container-input">
    <div class="box-input" :class="{'check': complete && !error, 'wrong': error}">
      <slot name="field"></slot>
      <component v-bind:is="iconComponent" size="16" class="icon--grey" v-if="empty || !complete"></component>
      <icon-check-circle size="16" class="blue-check" v-else-if="complete && !error"></icon-check-circle>
    </div>
    <p class="input-alert">
      <slot name="error"></slot>
    </p>
  </div>
</template>


<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import IconCheckCircle from '@/components/icons/icon-check-circle.vue'

type Icon = '';

@Component({
  components: {
    IconCheckCircle,
  }
})
export default class BasicInputStripe extends Vue {

  @Prop()
  icon?: Icon;

  @Prop({ default: false })
  error?: boolean

  @Prop({ default: false })
  complete?: boolean

  @Prop({ default: false })
  empty?: boolean

  get iconComponent(): Icon {
    return ''
  }
}
</script>

<style lang="scss" scoped>
.blue-check {
  color: $blue;
}

.container-input {
  .input-alert {
    font-size: $fs-xs;
    margin-top: 0.25rem;
    text-align: left;
    span {
      font-size: $fs-xs;
      margin-top: 0.25rem;
      text-align: left;
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
  padding: 0.625rem 0.75rem;

  &.wrong {
    animation: wrong-log 0.3s;
    border: 1px solid $orange;
  }
  &.check {
    border: 1px solid $blue;
    box-shadow: 0 0 3px 0 rgba(66, 99, 235, 0.5);
  }
  .StripeElement {
    font-size: 16px;
    line-height: 1.5;
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
  100% {
    left: 0px;
  }
  60% {
    left: 15px;
  }
  80% {
    left: -15px;
  }
}
</style>

