<script setup lang="ts">
const { t } = useI18n()
</script>

<template>
  <div class="landing-form-container">
    <LoginSignupText />
    <LoginSignupForm
      :bottom-text="t('sign-up.have-account')"
      :bottom-link-text="t('sign-up.have-account-link')"
      :submit-button-text="t('sign-up.submit-button')"
      bottom-link-route="/login"
      :submit-action="() => {}"
    >
      <LoginSignupFormInput :label="t('sign-up.username-label')" type="text" name="username" />
      <LoginSignupFormInput :label="t('sign-up.email-label')" type="email" name="email" />
      <LoginSignupFormInput :label="t('sign-up.password-label')" type="password" name="password" />
      <LoginSignupFormInput :label="t('sign-up.confirm-password-label')" type="password" name="confirm-password" />
    </LoginSignupForm>
  </div>
</template>

<style scoped lang="scss">
.landing-form-container {
  height: 100vh;
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
