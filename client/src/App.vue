<script setup lang="ts">
// https://github.com/vueuse/head
// you can use this to manipulate the document head in any components,
// they will be rendered correctly in the html results with vite-ssg
useHead({
  title: 'DashCode',
  meta: [
    { name: 'description', content: '' },
  ],
})

const { availableLocales, locale } = useI18n()

const locales = availableLocales
locale.value = locales[(locales.indexOf(locale.value) + 1) % locales.length]

</script>

<template>
  <RouterView />
</template>

<style lang="scss">
@import url('~/assets/scss/fonts.scss');
</style>
