<script setup lang="ts">
import useAuthStore from '~/store/useAuth'

const auth = useAuthStore()
const router = useRouter()
const { t } = useI18n()
</script>

<template>
  <ErrorIndicator />
  <main :class="auth.loggedIn ? '' : 'picture-bg'">
    <div v-if="auth.loggedIn">
      <Suspense v-if="auth.loggedIn">
        <template #default>
          <UserNotes />
        </template>
        <template #fallback>
          <LoadingData />
        </template>
      </Suspense>

      <NavigationPanel>
        <NavigationButton @on-press="router.push('/note/create')">
          <div class="i-carbon:add" /> {{ t('index.home.side-buttons.add-notes') }}
        </NavigationButton>
        <NavigationButton @on-press="router.push('/explore')">
          <div class="i-carbon:arrow-right" /> {{ t('index.home.side-buttons.explore') }}
        </NavigationButton>
      </NavigationPanel>
    </div>
    <LandingPage v-else />
  </main>
</template>

<style scoped lang="scss">
main {
  min-height: 100vh;
  background-color: #1A2641;

  &.picture-bg {
    background-image: url('~/assets/img/background-photo.webp');
    background-attachment: fixed;
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
  }
}
</style>

<route lang="yaml">
meta:
  requiresAuth: false
</route>
