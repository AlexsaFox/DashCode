<script setup lang="ts">
const { t } = useI18n()
const router = useRouter()
</script>

<template>
  <div class="main-container">
    <section class="content-container">
      <h1>{{ t('not-found.header') }}</h1>
      <p>{{ t('not-found.details') }}</p>
      <div class="button-container">
        <button @click="router.back()">
          {{ t('not-found.buttons.go-back') }}
        </button>
        <button @click="router.push('/')">
          {{ t('not-found.buttons.go-home') }}
        </button>
      </div>
    </section>
  </div>
</template>

<style scoped lang="scss">
.main-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100vw;
  height: 100vh;

  .content-container {
    max-width: 800px;
    text-align: center;

    h1 {
      font-family: 'ClearSans-Bold';
      font-size: 64px;
    }

    p {
      margin: 20px 0;
      font-family: 'ClearSans-Regular';
      font-size: 24px;
    }

    .button-container {
      display: flex;
      justify-content: center;
      align-items: center;

      button {
        margin: 0 10px;
        padding: 12px 36px;
        border-radius: 10px;
        font-size: 16px;
        color: var(--user-contrasting-color);
        background-color: var(--user-color);
        user-select: none;
        transition-duration: 0.2s;

        &:hover {
          opacity: 0.8;
        }
      }
    }
  }
}
</style>

<route lang="yaml">
meta:
  requiresAuth: true
</route>
