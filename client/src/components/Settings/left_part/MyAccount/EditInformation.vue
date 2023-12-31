<script setup lang="ts">
import { email, helpers, minLength, required, sameAs } from '@vuelidate/validators'
import { useVuelidate } from '@vuelidate/core'
import useAuthStore from '~/store/useAuth'
import checkFormErrors from '~/utils/checkFormErrors'

const { t } = useI18n()
const auth = useAuthStore()

const enabledEmailField = ref(false)
const showPasswordField = ref(false)

const formData = reactive({
  email: auth.user.email,
  newPassword: '',
  confirmPassword: '',
  currentPassword: '',
})

const rules = {
  email: {
    email: helpers.withMessage(t('settings.account.errors.email-invalid'), email),
  },
  confirmPassword: {
    sameAs: helpers.withMessage(
      t('settings.account.errors.passwords-do-not-match'),
      sameAs(computed(() => formData.newPassword)),
    ),
    minLength: helpers.withMessage(t('settings.account.errors.password-too-short'), minLength(8)),
  },
  currentPassword: {
    required: helpers.withMessage(t('settings.account.errors.password-required'), required),
  },
}

const vuelidate = useVuelidate(rules, formData)

function onSubmit() {
  checkFormErrors(
    vuelidate,
    () => { return auth.editAuth(formData.currentPassword, formData.email, formData.newPassword) },
    () => {
      formData.email = auth.user.email
      enabledEmailField.value = false
      showPasswordField.value = false
    },
  )
}

</script>

<template>
  <div class="information">
    <div class="stroke">
      <div class="left">
        <h2>{{ t("settings.email-label") }}</h2>
        <input
          id="input_email" v-model="formData.email" :disabled="!enabledEmailField" type="email"
          class="input email"
        >
      </div>
      <button v-if="!enabledEmailField" type="button" class="edit" @click="enabledEmailField = true">
        {{ t("settings.button.edit.label") }}
      </button>
    </div>
    <div v-if="showPasswordField">
      <div id="new_password_container" class="stroke password">
        <div class="left">
          <h2>{{ t("settings.new-password-label") }}</h2>
          <input v-model="formData.newPassword" type="password" class="input">
        </div>
      </div>
      <div id="confirm_password_container" class="stroke password">
        <div class="left">
          <h2>{{ t("settings.confirm-password-label") }}</h2>
          <input v-model="formData.confirmPassword" type="password" class="input">
        </div>
      </div>
    </div>

    <div v-if="showPasswordField || enabledEmailField">
      <div id="current_password_container" class="stroke password">
        <div class="left">
          <h2>{{ t("settings.current-password-label") }}</h2>
          <input v-model="formData.currentPassword" type="password" class="input">
        </div>
      </div>
    </div>
    <button
      v-if="!showPasswordField" type="button" class="change_password"
      @click="showPasswordField = true"
    >
      {{ t("settings.button.change-password-label") }}
    </button>

    <button v-if="showPasswordField || enabledEmailField" class="edit account" @click="onSubmit()">
      {{ t("settings.button.submit.changes-label") }}
    </button>
  </div>
</template>

<style scoped lang="scss">
.information {
  border-radius: 15px;
  background-color: #465586;
  margin: 3%;
  padding: 2% 4% 2% 2%;

  .stroke {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 1% 0%;

    .left {
      h2 {
        font-family: "ClearSans-Medium";
        font-size: 18px;
        color: rgba(255, 255, 255, 0.6);
        margin: 0%;
        font-weight: 500;
      }

      h3 {
        font-family: "ClearSans-Regular";
        font-size: 20px;
        color: rgba(255, 255, 255);
        margin: 0%;
        font-weight: 300;
      }
    }
  }

  .edit {
    border-radius: 5px;
    background-color: #223153;
    border: 0px;
    padding: 1% 2%;
    color: white;
    font-family: "ClearSans-Light";
    font-size: 20px;
    transition-duration: 0.2s;

    &:hover {
      background-color: #303d67;
    }
  }

  .edit.account {
    display: flex;
  }

  .input {
    background-color: #303d67;
    border: 0px;
    color: white;
    font-family: "ClearSans-Light";
    font-size: 20px;
    border: 2px #303d67;
    margin-top: 2%;
    width: auto;
    padding: 1% 2%;
    border-radius: 5px;

    &:disabled {
      background-color: #465586;
      border: 0px;
      color: white;
      font-family: "ClearSans-Light";

    }

    &:focus {
      background-color: #303d67;
      border: 0px;
      color: white;
      font-family: "ClearSans-Light";

      outline: 2px solid rgba(39, 55, 91);
    }

    &:-webkit-autofill {
      box-shadow: inset 0 0 0 50px #223153;
      -webkit-box-shadow: inset 0 0 0 50px #223153;
      -webkit-text-fill-color: white;
    }
  }
  .input.email{
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

.change_password {
  border: 0px;
  border-radius: 5px;
  background-color: var(--user-color);
  font-family: "ClearSans-Light";
  font-size: 18px;
  padding: 1% 3%;
  margin: 1% 0% 2%;
  color: var(--user-contrasting-color);
  transition-duration: 0.2s;

  &:hover {
    opacity: 0.8;
  }
}
</style>
