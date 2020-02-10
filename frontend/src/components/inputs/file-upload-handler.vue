<template>
  <div class="file-upload-handler">
    <input ref="input" aria-hidden class="file-upload-handler__input" type="file"  @change="change" :disabled="disabled">
    <slot></slot>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

@Component
export default class FileUploadHandler extends Vue {
  @Prop({ default: false })
  disabled!: boolean

  change(event: Event): void {
    const target = (event.target! as HTMLInputElement)
    this.$emit('change', (target.files || [])[0]);
  }
}
</script>

<style lang="scss" scoped>
.file-upload-handler {
  cursor: pointer;
  overflow: hidden;
  position: relative;

  input {
    cursor: pointer;

    &:disabled {
      cursor: not-allowed;
    }
  }

  .file-upload-handler__input {
    bottom: 0;
    left: 0;
    opacity: 0;
    position: absolute;
    right: 0;
    top: 0;
  }
}
</style>
