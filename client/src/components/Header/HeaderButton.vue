<script setup lang="ts">
interface Props {
  href: string
  bg?: string
  fg?: string
}

const { href, bg = 'transparent', fg = 'white' } = defineProps<Props>()

const router = useRouter()
function go(location: string) {
  router.push(`${encodeURIComponent(location)}`)
}
</script>

<template>
  <button @click="go(href)">
    <slot />
  </button>
</template>

<style scoped lang="scss">
@import url('../../assets/scss/fonts.scss');

button {
  margin: 0 6px;
  padding: 10px 32px;
  background-color: v-bind('bg');

  font-size: 20px;
  font-family: 'ClearSans-Regular';
  color: v-bind('fg');
  border-radius: 10px;
}
</style>
