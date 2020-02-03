<template>
    <span><slot></slot></span>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator';

@Component
export default class ErrorMessage extends Vue {
}
</script>

<style lang="scss" scoped>
span {
    color: $orange;
    font-size: $fs-xs;
}
</style>