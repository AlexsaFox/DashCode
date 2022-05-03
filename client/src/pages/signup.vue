<script setup lang="ts">
import { email, helpers, required, sameAs } from '@vuelidate/validators'
import { useVuelidate } from '@vuelidate/core'
import useAuthStore from '~/store/useAuth'
import useErrorsStore from '~/store/useErrors'

const { t } = useI18n()
const auth = useAuthStore()
const errors = useErrorsStore()

const credentials = reactive({
  username: '',
  email: '',
  password: '',
  confirm_password: '',
})

const rules = {
  username: {
    required: helpers.withMessage(t('sign-up.errors.username-required'), required),
  },
  email: {
    required: helpers.withMessage(t('sign-up.errors.email-invalid'), required),
    email: helpers.withMessage(t('sign-up.errors.email-invalid'), email),
  },
  password: {
    required: helpers.withMessage(t('sign-up.errors.password-required'), required),
  },
  confirm_password: {
    sameAs: helpers.withMessage(
      t('sign-up.errors.passwords-do-not-match'),
      sameAs(computed(() => credentials.password)),
    ),
  },
}

const vuelidate = useVuelidate(rules, credentials)

function onSubmit() {
  errors.$reset()
  vuelidate.value.$touch()

  if (vuelidate.value.$error) {
    for (const error of vuelidate.value.$errors)
      errors.addError(error.$message.toString())
  }
  else {
    auth.register(credentials.username, credentials.email, credentials.password)
  }
}
</script>

<template>
  <LoginSignupForm
    :bottom-text="t('sign-up.have-account')"
    :bottom-link-text="t('sign-up.have-account-link')"
    :submit-button-text="t('sign-up.submit-button')"
    bottom-link-route="/login"
    :submit-action="onSubmit"
  >
    <LoginSignupFormInput
      v-model="credentials.username"
      :label="t('sign-up.labels.username')"
      type="text"
    />
    <LoginSignupFormInput
      v-model="credentials.email"
      :label="t('sign-up.labels.email')"
      type="email"
    />
    <LoginSignupFormInput
      v-model="credentials.password"
      :label="t('sign-up.labels.password')"
      type="text"
    />
    <LoginSignupFormInput
      v-model="credentials.confirm_password"
      :label="t('sign-up.labels.confirm-password')"
      type="text"
    />
  </LoginSignupForm>
</template>

<route lang="yaml">
meta:
  layout: login-signup
</route>
