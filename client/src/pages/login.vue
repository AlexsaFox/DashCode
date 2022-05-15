<script setup lang="ts">
import { helpers, required } from '@vuelidate/validators'
import { useVuelidate } from '@vuelidate/core'
import useAuthStore from '~/store/useAuth'
import checkFormErrors from '~/utils/checkFormErrors'

const { t } = useI18n()
const auth = useAuthStore()
const router = useRouter()

const credentials = reactive({
  username: '',
  password: '',
})

const rules = {
  username: {
    required: helpers.withMessage(t('login.errors.username-required'), required),
  },
  password: {
    required: helpers.withMessage(t('login.errors.password-required'), required),
  },
}

const vuelidate = useVuelidate(rules, credentials)

function onSubmit() {
  checkFormErrors(
    vuelidate,
    () => { return auth.login(credentials.password, credentials.username, credentials.username) },
    () => { router.push('/') },
  )
}
</script>

<template>
  <LoginSignupForm
    :bottom-text="t('login.no-account')" :bottom-link-text="t('login.no-account-link')"
    :submit-button-text="t('login.submit-button')" bottom-link-route="/signup" :submit-action="onSubmit"
  >
    <LoginSignupFormInput v-model="credentials.username" :label="t('login.labels.username')" type="text" />
    <LoginSignupFormInput v-model="credentials.password" :label="t('login.labels.password')" type="password" />
  </LoginSignupForm>
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
  layout: login-signup
</route>
