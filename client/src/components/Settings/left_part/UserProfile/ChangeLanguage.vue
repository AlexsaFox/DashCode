<script setup lang="ts">
import useAuthStore from '~/store/useAuth'

const { t } = useI18n()

const auth = useAuthStore()
const chosenLocale = ref(auth.locale)

function changeLocale() {
  auth.changeLocale(chosenLocale.value)
}
</script>

<template>
  <div class="profile_language">
    <h3>{{ t('settings.user-profile.header.change-language') }}</h3>
    <h4>{{ t("settings.change-language-label") }}</h4>
    <div class="bottom_line">
      <select v-model="chosenLocale" class="dropdown">
        <option class="lang" value="en">
          {{ t("settings.languages.english-label") }}
        </option>
        <option class="lang" value="fr">
          {{ t("settings.languages.french-label") }}
        </option>
        <option class="lang" value="de">
          {{ t("settings.languages.german-label") }}
        </option>
        <option class="lang" value="es">
          {{ t("settings.languages.spanish-label") }}
        </option>
        <option class="lang" value="ru">
          {{ t("settings.languages.russian-label") }}
        </option>
      </select>
      <button class="edit" @click="changeLocale()">
        {{ t("settings.button.submit.color-label") }}
      </button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.profile_language {
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

    .dropdown {
      background-color: #303D67;
      padding: 2% 4%;
      border-radius: 10px;
      font-size: 20px;
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
