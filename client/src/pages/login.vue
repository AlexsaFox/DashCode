<script setup lang="ts">
const { t } = useI18n()
</script>

<template>
  <div class="landing-form-container">
    <LoginSignupText />
    <LoginSignupForm
      :bottom-text="t('login.no-account')"
      :bottom-link-text="t('login.no-account-link')"
      :submit-button-text="t('login.submit-button')"
      bottom-link-route="/signup"
      :submit-action="() => {}"
    >
      <LoginSignupFormInput :label="t('login.username-label')" type="text" name="username" />
      <LoginSignupFormInput :label="t('login.password-label')" type="password" name="password" />
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
