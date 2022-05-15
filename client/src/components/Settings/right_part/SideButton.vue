<script setup lang="ts">
const emit = defineEmits<{
  (e: 'buttonClick'): void
}>()
</script>

<template>
  <button class="standard-button" @click="emit('buttonClick')">
    <slot />
  </button>
</template>
