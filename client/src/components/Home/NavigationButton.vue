<script setup lang="ts">
const emit = defineEmits<{
  (e: 'onPress'): void
}>()
</script>

<template>
  <button class="standard_button" @click="emit('onPress')">
    <slot />
  </button>
</template>

<style scoped lang=scss>
@import "/src/assets/scss/standard-button.scss";

.standard_button {
  @include standard-button;
  width: 100%;
}
</style>
