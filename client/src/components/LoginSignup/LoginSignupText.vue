<script setup lang="ts">
const { t } = useI18n()
</script>

<template>
  <div class="text-container">
    <h1>DashCode</h1>
    <p>{{ t('login-sign-up.text') }}</p>
  </div>
</template>

<style scoped lang="scss">
@import './block-parts.scss';

.text-container {
  @include block-part;

  h1 {
    font-family: 'ClearSans-Bold';
    font-size: 64px;
    color: white;
  }
  p {
    font-family: 'ClearSans-Bold';
    text-align: justify;
    font-size: 22px;
    color: white;
  }
}
</style>
