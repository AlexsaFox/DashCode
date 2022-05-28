<script setup lang="ts">
import noteEditActions from '~/constants/types/noteEditActions'
const { t } = useI18n()

const emit = defineEmits<{
  (e: 'action', action: noteEditActions): void
}>()

function cancel() { emit('action', noteEditActions.cancel) }
function discard() { emit('action', noteEditActions.discard) }
function save() { emit('action', noteEditActions.save) }
</script>

<template>
  <modal @close-popup="cancel">
    <header>
      <h3>{{ t('note-show.delete-warning.header') }}</h3>
    </header>
    <p>{{ t("note-edit.warning-label") }}</p>
    <div class="button-container">
      <button @click="save">
        {{ t('note-edit.save-button') }}
      </button>
      <button @click="discard">
        {{ t('note-edit.unsave-button') }}
      </button>
      <button @click="cancel">
        {{ t('note-edit.cancel-button') }}
      </button>
    </div>
  </modal>
</template>
