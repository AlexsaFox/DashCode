<script setup lang="ts">
import useAuthStore from '~/store/useAuth'

const { t } = useI18n()
const router = useRouter()
const auth = useAuthStore()
</script>

<template>
  <div class="crutch">
    <Suspense>
      <template #default>
        <PublicNotes />
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
        @on-press="router.push('/')"
      >
        <div class="i-carbon:home" /> {{ t('index.home.side-buttons.go-home') }}
      </NavigationButton>
      <NavigationButton
        v-if="auth.user.isSuperuser"
        @on-press="router.push('/admin')"
      >
        <div class="i-carbon:police" /> {{ t('index.home.side-buttons.admin') }}
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
</route>
