<template>
  <div class="loader">
    <div class="progress-steps">
      <span>Driver Records</span>
      <span>Vehicle Records</span>
      <span>Policy Options</span>
    </div>
    <div class="progress-bar">
      <div class="progress-bar--center" :class="{'active':secondStep}"></div>
      <div class="progress-bar__percent" :class="{'percent':firstStep,'finish':thirdStep}"></div>
    </div>
    <p>{{message}}</p>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

@Component
export default class LoadingQuote extends Vue {
  firstStep = false
  secondStep = false
  thirdStep = false
  message = 'Searching for Driver Records…'

  created(): void {
    setTimeout(() => {
      this.firstStep = true;
    }, 1000);
    setTimeout(() => {
      this.secondStep = true;
      this.message = 'Searching for Vehicle Records…';
    }, 3000);
    setTimeout(() => {
      this.thirdStep = true;
      this.message = 'Searching for Policy Options…';
    }, 5000);
    setTimeout(() => {
      this.$emit('done')
    }, 7200);
  }
}
</script>

<style lang="scss" scoped>
.loader {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 2.5rem;
}
p {
  font-size: $fs-lg;
  margin-top: 2rem;
}
.progress-steps {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  width: 32rem;
  span {
    font-size: $fs-sm;
    opacity: 0.5;
  }
}
.progress-bar {
  background-color: $grey-medium;
  border-radius: 10.5px;
  height: 0.75rem;
  position: relative;
  width: 32rem;
  &::before,
  &::after,
  .progress-bar--center {
    background-color: $grey-medium;
    border-radius: 50%;
    content: "";
    height: 1.125rem;
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 1.125rem;
  }
  &::before {
    left: 0;
  }
  &::after {
    right: 0;
  }
  .progress-bar--center {
    right: 50%;
    transform: translate(50%, -50%);
    &::before {
      background-color: $blue;
      border-radius: 50%;
      content: "";
      display: none;
      height: 0.625rem;
      position: absolute;
      left: 4px;
      top: 50%;
      transform: translateY(-50%);
      width: 0.625rem;
      z-index: 1;
    }
    &.active {
      &::before {
        display: block;
      }
    }
  }
  .progress-bar__percent {
    background-color: $blue;
    border-radius: 10.5px;
    margin: 3px 3px;
    height: 6px;
    position: relative;
    z-index: 1;
    width: 1rem;
    &.percent {
      animation: progress-50 2s;
      width: 15.75rem;
    }
    &.finish {
      animation: progress-100 2s;
      width: 31.5rem;
      &::after {
        display: block;
      }
    }
    &::before,
    &::after {
      background-color: $blue;
      border-radius: 50%;
      content: "";
      height: 0.625rem;
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      width: 0.625rem;
      z-index: 1;
    }
    &::before {
      left: 0;
    }
    &::after {
      right: 0;
      display: none;
    }
  }
}
@keyframes progress-50 {
  0% {
    width: 1rem;
  }
  100% {
    width: 15.75rem;
  }
}
@keyframes progress-100 {
  0% {
    width: 15.75rem;
  }
  100% {
    width: 31.5rem;
  }
}
</style>
