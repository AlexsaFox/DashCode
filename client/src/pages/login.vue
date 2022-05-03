<script setup lang="ts">
import { useAuthStore } from '~/store/useAuth'

const credentials = ref({
  username: '',
  password: '',
})
const { t } = useI18n()

const auth = useAuthStore()

function onSubmit() {
  auth.login(credentials.value.password, credentials.value.username, credentials.value.username)
}
</script>

<template>
  <div class="landing-form-container">
    <LoginSignupText />
    <LoginSignupForm
      :bottom-text="t('login.no-account')"
      :bottom-link-text="t('login.no-account-link')"
      :submit-button-text="t('login.submit-button')"
      bottom-link-route="/signup"
      :submit-action="onSubmit"
    >
      <LoginSignupFormInput
        :label="t('login.username-label')"
        type="text"
        name="username"
        @changed="(username) => credentials.username = username"
      />
      <LoginSignupFormInput
        :label="t('login.password-label')"
        type="password"
        name="password"
        @changed="(passwd) => credentials.password = passwd"
      />
    </LoginSignupForm>
  </div>
</template>

<style scoped lang="scss">
.landing-form-container {
  height: 100%;
  width: 100%;
  padding: 0 300px;
  display: flex;
  justify-content: space-around;
  align-items: center;
}
</style>

<route lang="yaml">
meta:
  layout: landing
</route>
