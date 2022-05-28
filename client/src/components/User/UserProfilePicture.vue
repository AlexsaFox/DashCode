<script setup lang="ts">
import useAuthStore from '~/store/useAuth'
import config from '~/constants/config'

const { filename } = defineProps<{
  filename?: string
}>()
const filenameRef = ref(filename)

if (filenameRef.value === undefined)
  filenameRef.value = useAuthStore().user.profilePictureFilename
</script>

<template>
  <!-- Multiple elements, so webpack will catch default picture in build -->
  <img v-if="filenameRef === null" v-bind="$attrs" src="/src/assets/img/default-profile-picture.jpg">
  <img v-else v-bind="$attrs" :src="`${config.api_host}/uploads/${filenameRef}`">
</template>
