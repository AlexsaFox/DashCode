<script setup lang="ts">
import { helpers, required } from '@vuelidate/validators'
import { useVuelidate } from '@vuelidate/core'
import checkFormErrors from '~/utils/checkFormErrors'
import useAuthStore from '~/store/useAuth'

const { t } = useI18n()
const auth = useAuthStore()
const router = useRouter()

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
    () => { return auth.deleteAccount(passwordForm.password) },
    () => { router.push('/') },
  )
}
</script>

<template>
  <div class="overlay">
    <div class="popup">
      <div class="header">
        <span>{{ t("settings.account_removal.warning.header") }}</span>
        <button class="close" @click="emit('closePopup')">
          &times;
        </button>
      </div>
      <div class="content">
        <span class="text">{{ t("settings.account_removal.warning.text") }}</span>
        <div class="stroke">
          <div class="left">
            <h2>{{ t("settings.current-password-label") }}</h2>
            <input v-model="passwordForm.password" type="password" class="input">
          </div>
          <button type="submit" class="send_button" @click="onSubmit">
            {{ t("settings.button.submit.changes-label") }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.overlay {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7);
  transition: opacity 500ms;
  height: 100%;
  z-index: 10;
  overflow-y: auto;
}

.popup {
  margin: 70px auto;
  background: #303d67;
  border-radius: 10px;
  width: 50%;
  position: relative;
  padding: 2%;

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .close {
    transition: all 200ms;
    font-size: 50px;
    text-decoration: none;
    color: white;

    &:hover {
      color: #465586;
    }

  }

  span {
    font-family: 'ClearSans-Medium';
    color: #fa3b3b;
    font-size: 24px;
  }

  .content {
    display: flex;
    flex-direction: column;
    font-family: 'ClearSans-Regular';
    color: white;
    padding: 0px 3%;
    max-height: 40%;
    overflow: auto;
    background-color: #303d67;
    border-radius: 0 0 10px 10px;
    display: flex;
    flex-direction: column;
    align-items: center;

    .text {
      font-family: 'ClearSans-Medium';
      color: white;
      font-size: 24px;
    }

    .stroke {
      display: flex;
      justify-content: space-around;
      align-items: center;
      margin: 3% 0%;
      width: 100%;

      h2 {
        font-family: "ClearSans-Medium";
        font-size: 18px;
        color: rgba(255, 255, 255, 0.6);
        margin: 0%;
        font-weight: 500;
      }

      .input {
        background-color: #223153;
        border: 0px;
        color: white;
        font-family: "ClearSans-Light";
        font-size: 20px;
        border: 2px #223153;
        margin-top: 2%;
        width: auto;
        padding: 1% 2%;
        border-radius: 5px;
        margin-bottom: 2%;

        &:focus {
          background-color: #223153;
          border: 0px;
          color: white;
          font-family: "ClearSans-Light";

          outline: 2px solid rgba(39, 55, 91);
        }

        &:-webkit-autofill {
          box-shadow: inset 0 0 0 50px #223153;
          -webkit-box-shadow: inset 0 0 0 50px #223153;
          /* цвет вашего фона */
          -webkit-text-fill-color: white;
          /* цвет текста */
        }
      }
    }

    .send_button {
      font-family: "ClearSans-Regular";
      color: white;
      margin-top: 3%;
      padding: 12px 16px;
      background: #223153;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      font-size: 20px;
      transition-duration: 0.2s;

      &:hover {
        background: #303d67;
      }

      &:disabled {
        opacity: 0.6;
      }

      &:disabled:hover {
        background: #465586;
      }
    }
  }
}

.fileform {
  background-color: #223153;
  width: 100%;
  height: 7vh;
  padding: 1%;
  margin-top: 6px;
  border-radius: 10px;
  position: relative;
  cursor: pointer;
  overflow: hidden;
  vertical-align: middle;
  text-align: left;
  display: flex;

  #fileformlabel {
    display: flex;
    align-items: center;
    background-color: #223153;
    float: left;
    height: auto;
    overflow: hidden;
    padding: 1%;
    font-size: 16px;
    width: 100%;
  }

  .selectbutton {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: var(--user-color);
    border-radius: 5px;
    color: var(--user-contrasting-color);
    // float: right;
    font-size: 18px;
    height: auto;
    padding: 3%;
    width: 15%;
  }

  input {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    -moz-opacity: 0;
    filter: alpha(opacity=0);
    opacity: 0;
    height: 100%;
    z-index: 20;
    padding: 0;
    margin: 0;
    cursor: pointer;
  }
}
</style>
