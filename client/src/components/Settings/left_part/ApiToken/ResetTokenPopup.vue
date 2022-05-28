<script setup lang="ts">
import { helpers, required } from '@vuelidate/validators'
import { useVuelidate } from '@vuelidate/core'
import checkFormErrors from '~/utils/checkFormErrors'
import useAuthStore from '~/store/useAuth'

const { t } = useI18n()
const auth = useAuthStore()

const emit = defineEmits<{
  (e: 'closePopup'): void
}>()

const passwordForm = reactive({
  password: '',
})
const rules = {
  password: {
    required: helpers.withMessage(
      t('settings.account.errors.password-required'),
      required,
    ),
  },
}

const vuelidate = useVuelidate(rules, passwordForm)

function onSubmit() {
  checkFormErrors(
    vuelidate,
    () => { return auth.resetToken(passwordForm.password) },
    () => { emit('closePopup') },
  )
}
</script>

<template>
  <modal @close-popup="emit('closePopup')">
    <header>
      <h3 class="warning">
        {{ t('note-show.delete-warning.header') }}
      </h3>
    </header>
    <p>{{ t("settings.token.reset-warning") }}</p>
    <div class="confirm-password-container">
      <p>{{ t("settings.current-password-label") }}</p>
      <input v-model="passwordForm.password" type="password" class="input">
    </div>
    <div class="button-container space-between">
      <button @click="onSubmit">
        {{ t("settings.button.submit.changes-label") }}
      </button>
    </div>
  </modal>
</template>
