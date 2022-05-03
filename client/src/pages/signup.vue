<script setup lang="ts">
import { useAuthStore } from '~/store/useAuth'

const { t } = useI18n()

const credentials = ref({
  username: '',
  email: '',
  password: '',
  confirm_password: '',
})

const auth = useAuthStore()

function onSubmit() {
  if (credentials.value.password !== credentials.value.confirm_password) {
    // TODO: implement a proper error handler
    // eslint-disable-next-line no-console
    console.log('Password and confirm password fields do not match')
    return
  }

  auth.register(credentials.value.username, credentials.value.email, credentials.value.password)
}
</script>

<template>
  <div class="landing-form-container">
    <LoginSignupText />
    <LoginSignupForm
      :bottom-text="t('sign-up.have-account')"
      :bottom-link-text="t('sign-up.have-account-link')"
      :submit-button-text="t('sign-up.submit-button')"
      bottom-link-route="/login"
      :submit-action="onSubmit"
    >
      <LoginSignupFormInput
        :label="t('sign-up.username-label')"
        type="text"
        @changed="(username) => credentials.username = username"
      />
      <LoginSignupFormInput
        :label="t('sign-up.email-label')"
        type="email"
        @changed="(email) => credentials.email = email"
      />
      <LoginSignupFormInput
        :label="t('sign-up.password-label')"
        type="password"
        @changed="(passwd) => credentials.password = passwd"
      />
      <LoginSignupFormInput
        :label="t('sign-up.confirm-password-label')"
        type="password"
        @changed="(passwd) => credentials.confirm_password = passwd"
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
