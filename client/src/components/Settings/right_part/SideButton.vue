<script setup lang="ts">
defineProps<{
  icon: string
  text: string
}>()
const emit = defineEmits<{
  (e: 'buttonClick'): void
}>()
</script>

<template>
  <button class="standart_button" @click="emit('buttonClick')">
    <div :class="`i-${icon}`" />{{ text }}
  </button>
</template>
