<script setup lang="ts">
import useAuthStore from '~/store/useAuth'

const auth = useAuthStore()
</script>

<template>
  <HomePage v-if="auth.loggedIn" />
  <LandingPage v-else />
</template>
