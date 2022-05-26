<script setup lang="ts">
// https://github.com/vueuse/head
// you can use this to manipulate the document head in any components,

import { storeToRefs } from 'pinia'
import { getContrastingColor } from './utils/colors'
import useAuthStore from './store/useAuth'

// they will be rendered correctly in the html results with vite-ssg
useHead({
  title: 'DashCode',
  meta: [{ name: 'description', content: '' }],
})

const { loggedIn, user } = storeToRefs(useAuthStore())
const userProfileColor = computed(() => {
  return loggedIn.value ? user.value.profileColor : '#9e6dee'
})
const userProfileContrastingColor = computed(() => {
  return getContrastingColor(userProfileColor.value)
})
</script>

<template>
  <RouterView />
</template>

<style lang="scss">
::-webkit-scrollbar {
  width: 20px;
}

::-webkit-scrollbar-track {
  background-color: #1a2641;
}

::-webkit-scrollbar-thumb {
  background-color: #303d67;
  border-radius: 10px;
}
@import url('~/assets/scss/fonts.scss');

* {
  --user-color: v-bind(userProfileColor);
  --user-contrasting-color: v-bind(userProfileContrastingColor);
}
</style>
