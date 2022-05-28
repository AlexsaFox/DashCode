<script setup lang="ts">
const { t } = useI18n()
const router = useRouter()
</script>

<template>
  <div class="crutch">
    <Suspense>
      <template #default>
        <AllNotes />
      </template>
      <template #fallback>
        <LoadingData />
      </template>
    </Suspense>

    <NavigationPanel>
      <NavigationButton
        @on-press="router.push('/note/create')"
      >
        <div class="i-carbon:add" /> {{ t('index.home.side-buttons.add-notes') }}
      </NavigationButton>
      <NavigationButton
        @on-press="router.push('/explore')"
      >
        <div class="i-carbon:arrow-right" /> {{ t('index.home.side-buttons.explore') }}
      </NavigationButton>
      <NavigationButton
        @on-press="router.push('/')"
      >
        <div class="i-carbon:home" /> {{ t('index.home.side-buttons.go-home') }}
      </NavigationButton>
    </NavigationPanel>
  </div>
</template>

<style scoped lang="scss">
.crutch {
  border: 1px solid transparent;
}
</style>

<route lang="yaml">
meta:
  requiresAuth: true
  requiresSuperuser: true
</route>
