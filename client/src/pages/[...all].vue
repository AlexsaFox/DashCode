<script setup lang="ts">
const { t } = useI18n()
const router = useRouter()

router.push('/not-found')
</script>

<template>
  <div class="main-container">
    <section class="content-container">
      <p>{{ t('not-found.click-here.details') }} <a>{{ t('not-found.click-here.link') }}</a></p>
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
    max-width: 660px;
    text-align: center;

    p {
      margin: 20px 0;
      font-family: 'ClearSans-Regular';
      font-size: 24px;

      a {
        text-decoration: underline;
        transition-duration: 0.2s;

        &:hover {
          color: var(--user-color);
          cursor: pointer;
          text-decoration: underline wavy;
        }
      }
    }
  }
}
</style>

<route lang="yaml">
meta:
  requiresAuth: false
</route>
