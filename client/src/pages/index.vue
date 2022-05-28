<script setup lang="ts">
import useAuthStore from '~/store/useAuth'

const auth = useAuthStore()
</script>

<template>
  <ErrorIndicator />
  <main :class="auth.loggedIn ? '' : 'picture-bg'">
    <Suspense v-if="auth.loggedIn">
      <template #default>
        <HomePage />
      </template>
      <template #fallback>
        <h1>Loading...</h1>
      </template>
    </Suspense>
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

<route lang="yaml">
meta:
  requiresAuth: false
</route>
