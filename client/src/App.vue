<script setup lang="ts">
// https://github.com/vueuse/head
// you can use this to manipulate the document head in any components,
// they will be rendered correctly in the html results with vite-ssg
useHead({
  title: 'DashCode',
  meta: [{ name: 'description', content: '' }],
})

const { availableLocales, locale } = useI18n()

const locales = availableLocales
locale.value = locales[(locales.indexOf(locale.value) + 1) % locales.length]

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
</style>
