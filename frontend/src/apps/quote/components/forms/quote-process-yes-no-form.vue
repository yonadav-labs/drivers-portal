<template>
    <div class='question-container'>
        <p class='question-container__explain'><slot></slot></p>
        <div class="question-container__yes-no">
          <basic-button
            @click.stop.prevent="$emit('yes')"
            text='Yes'
            :color='colorBlue'
            >
            <icon-check size='16' class='icon--blue'></icon-check>
          </basic-button>
          <basic-button
            text='No'
            :color='colorOrange'
            @click.stop.prevent="$emit('no')"
            >
            <icon-cross size='16' class='icon--orange'></icon-cross>
          </basic-button>
        </div>        
    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BasicButton from '@/components/buttons/basic-button.vue'
import IconCheck from '@/components/icons/icon-check.vue'
import IconCross from '@/components/icons/icon-cross.vue'

import { Colors } from '@/utils/colors'

@Component({
  components: {
    BasicButton, IconCheck, IconCross
  }
})
export default class QuoteProcessRadioForm extends Vue {
  
  get colorBlue(): string {
    return Colors.Blue
  }

  get colorOrange(): string {
    return Colors.Orange
  }
}
</script>

<style lang='scss' scoped>
.question-container {
  padding: 1.875rem 5.625rem 1.75rem;
  text-align: center;

  .question-container__explain {
    line-height: 1.5;
    font-size: $fs-lg;
    margin-left: auto;
    margin-right: auto;

    span {
      font-weight: $fw-semibold;
    }
  }

  .question-container__yes-no {
    align-items: center;
    display: flex;
    flex: 1;
    flex-direction: row-reverse;
    justify-content: center;
    margin-top: 1.75rem;
  }

  .question-content {
    background-color: $grey-opacity;
    border-radius: 8px;
    margin: 1.25rem auto;

    &.question-content--success {
      padding: 1.25rem 1.5rem;
      text-align: left;
    }
  }
}
</style>
