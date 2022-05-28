<script setup lang="ts">
const { t } = useI18n()

const emit = defineEmits<{
  (e: 'closePopup'): void
  (e: 'deleteNote'): void
}>()
</script>

<template>
  <modal @close-popup="emit('closePopup')">
    <header>
      <h3>{{ t('note-show.delete-warning.header') }}</h3>
    </header>
    <p>{{ t('note-show.delete-warning.details') }}</p>
    <div class="button-container">
      <button @click="emit('deleteNote')">
        {{ t('note-show.delete-warning.continue') }}
      </button>
      <button @click="emit('closePopup')">
        {{ t('note-show.delete-warning.cancel') }}
      </button>
    </div>
  </modal>
</template>
