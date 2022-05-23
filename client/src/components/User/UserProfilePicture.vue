<script setup lang="ts">
import useAuthStore from '~/store/useAuth'
const profilePicture = useAuthStore().profilePicture
</script>

<template>
  <!-- Multiple elements, so webpack will catch default picture in build -->
  <img v-if="profilePicture === null" v-bind="$attrs" src="/src/assets/img/default-profile-picture.jpg">
  <img v-else v-bind="$attrs" :src="profilePicture">
</template>
