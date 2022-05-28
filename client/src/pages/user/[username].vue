<script setup lang="ts">

const { t } = useI18n()
const router = useRouter()

const { username } = defineProps<{ username: string }>()
</script>

<template>
  <Suspense>
    <template #default>
      <PublicProfile
        :username="username"
        @loading-failed="router.replace('/not-found')"
      />
    </template>
    <template #fallback>
      <h1>Loading</h1>
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
</template>

<route lang="yaml">
meta:
  requiresAuth: true
</route>
