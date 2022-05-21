<script setup lang="ts">
import { helpers, required } from '@vuelidate/validators'
import { useVuelidate } from '@vuelidate/core'
import useAuthStore from '~/store/useAuth'
import checkFormErrors from '~/utils/checkFormErrors'

const { t } = useI18n()
const auth = useAuthStore()
const router = useRouter()

const editUsernameField = ref(false)
const usernameForm = reactive({
  username: auth.user.user.username,
})

const rules = {
  username: {
    required: helpers.withMessage(t('settings.profile.errors.username-required'), required),
  },
}

const vuelidate = useVuelidate(rules, usernameForm)

function onSubmit() {
  checkFormErrors(vuelidate, () => { return auth.edit(undefined, usernameForm.username) }, () => {
    router.go(0)
  })
}
</script>

<template>
  <div class="stroke username">
    <div class="edit_username">
      <div class="left">
        <h2>{{ t("settings.username-label") }}</h2>
        <input v-model="usernameForm.username" :disabled="!editUsernameField" class="input username">
      </div>
    </div>
    <button v-if="!editUsernameField" type="button" class="edit username" @click="editUsernameField = true">
      {{ t("settings.button.edit.label") }}
    </button>
    <button v-if="editUsernameField" class="edit name" @click="onSubmit">
      {{ t("settings.button.submit.changes-label") }}
    </button>
  </div>
</template>

<style scoped lang="scss">
.edit_username {
  display: flex;

  h2 {
    font-family: "ClearSans-Medium";
    font-size: 16px;
    color: rgba(255, 255, 255, 0.6);
    margin: 0%;
    font-weight: 500;
  }
}

.edit {
  border-radius: 5px;
  background-color: #223153;
  border: 0px;
  padding: 1% 2%;
  color: white;
  font-family: 'ClearSans-Light';
  font-size: 20px;
}

.edit.name {
  // display: none;
  border-radius: 5px;
  background-color: #223153;
  border: 0px;
  padding: 1% 2%;
  color: white;
  font-family: 'ClearSans-Light';
  font-size: 20px;
}

.stroke.username {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: auto;
  margin: 3% 2% 3% 4%;
}

.input {
  background-color: #465586;
  border: 0px;
  padding: 1%;
  border-radius: 5px;
  color: white;
  font-family: "ClearSans-Light";
  font-size: 22px;
  border: 2px #303d67;
  margin-top: 2%;
  width: auto;

  &:disabled {
    background-color: #303d67;
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

  & :-webkit-autofill {
    -webkit-box-shadow: inset 0 0 0 50px #223153;
    /* цвет вашего фона */
    -webkit-text-fill-color: white;
    /* цвет текста */
  }
}
</style>
