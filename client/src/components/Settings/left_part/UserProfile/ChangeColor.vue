<script setup lang="ts">
import { helpers, required } from '@vuelidate/validators'
import { useVuelidate } from '@vuelidate/core'
import useAuthStore from '~/store/useAuth'
import checkFormErrors from '~/utils/checkFormErrors'

const { t } = useI18n()
const auth = useAuthStore()
const router = useRouter()

const colorForm = reactive({
  color: auth.user.user.profileColor,
})

const rules = {
  color: {
    required: helpers.withMessage(t('settings.profile.errors.profile-color-required'), required),
    regexp: helpers.withMessage(t('settings.profile.errors.profile-color-bad-format'), helpers.regex(/^\#[0-9a-fA-F]{6}$/)),
  },
}

const vuelidate = useVuelidate(rules, colorForm)

function onSubmit() {
  checkFormErrors(vuelidate, () => { return auth.edit(colorForm.color, undefined) }, () => {
    router.go(0)
  })
}
</script>

<template>
  <div class="profile_color">
    <h3>{{ t('settings.user-profile.header.change-profile-color') }}</h3>
    <h4>{{ t("settings.change-color-label") }}</h4>
    <div class="bottom_line">
      <input v-model="colorForm.color" type="color" class="change_profile_color">
      <button class="edit" @click="onSubmit">
        {{ t("settings.button.submit.color-label") }}
      </button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.profile_color {
  width: 50%;
  h3 {
    font-family: "ClearSans-Medium";
    color: rgba(255, 255, 255, 0.6);
    font-weight: 100;
    margin-bottom: 2%;
    font-size: 20px;
  }

  .bottom_line {
    display: flex;
    justify-content: flex-start;
    gap: 5%;
    align-items: center;
    width: 100%;
    margin-top: 3%;

    .input {
      background-color: #465586;
      border: 0px;
      padding: 1%;
      border-radius: 5px;
      color: white;

      &:focus {
        outline: none;
      }
    }

    .edit {
      border-radius: 5px;
      background-color: #303D67;
      border: 0px;
      padding: 2% 2%;
      color: white;
      font-family: 'ClearSans-Light';
      font-size: 20px;
      width: 20%;
    }

    .change_profile_color {
      width: 50%;
      height: 7vh;
      border: none;
      border-radius: 10px;
      padding: 0;
      background-color: #223153;

      &::-webkit-color-swatch {
        border: none;
        border-radius: 10px;
      }
    }
  }

  h4 {
    font-family: 'ClearSans-Regular';
    color: rgba(255, 255, 255, 0.6);
    font-weight: 100;
    width: 600px;
    font-size: 20px;
  }
}
</style>
