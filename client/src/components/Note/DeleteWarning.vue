<script setup lang="ts">
const { t } = useI18n()

const emit = defineEmits<{
  (e: 'closePopup'): void
  (e: 'deleteNote'): void
}>()
</script>

<template>
  <div class="overlay">
    <section class="container">
      <button class="close" @click="emit('closePopup')">
        &times;
      </button>

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
    </section>
  </div>
</template>

<style lang="scss">
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  background: rgba(0, 0, 0, 0.7);
  transition: opacity 500ms;
  z-index: 10;

  display: flex;
  justify-content: center;
  align-items: center;

  .container {
    position: relative;
    background-color: #303d67;
    border-radius: 10px;
    padding: 50px;

    .close {
      position: absolute;
      font-size: 50px;
      top: -15px;
      right: 10px;
      color: white;
      transition-duration: 0.2s;

      &:hover {
        opacity: 0.7;
      }
    }

    header {
      display: flex;
      justify-content: center;
      align-items: center;

      h3 {
        font-size: 32px;
      }
    }

    p {
      font-size: 20px;
      margin: 20px 0;
    }

    .button-container {
      display: flex;
      justify-content: center;
      align-items: center;

      button {
        padding: 6px 24px;
        font-size: 16px;
        margin: 0 10px;
        border-radius: 10px;
        background-color: var(--user-color);
        color: var(--user-contrasting-color);
        transition-duration: 0.2s;

        &:hover {
          opacity: 0.8;
        }
      }
    }
  }
}
</style>
