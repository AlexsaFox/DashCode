<script setup lang="ts">
import useAuthStore from '~/store/useAuth'

const auth = useAuthStore()
</script>

<template>
  <ErrorIndicator />
  <main :class="auth.loggedIn ? '' : 'picture-bg'">
    <HomePage v-if="auth.loggedIn" />
    <LandingPage v-else />
  </main>
</template>

<style scoped lang="scss">
main {
  min-height: 100vh;
  background-color: #1A2641;

  &.picture-bg {
    background-image: url('~/assets/img/background-photo.webp');
    background-attachment: fixed;
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
  }
}
</style>
