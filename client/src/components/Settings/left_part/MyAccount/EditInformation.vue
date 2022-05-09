<script setup lang="ts">

const { t } = useI18n()

const enabledEmailField = ref(false)
const showPasswordField = ref(false)

</script>

<template>
  <div class="information">
    <div class="stroke">
      <div class="left">
        <h2>{{ t("settings.email-label") }}</h2>
        <input
          id="input_email" :disabled="!enabledEmailField" type="email" class="input email"
          value="expampleexpampleexpampleexpample@email.com"
        >
      </div>
      <button v-if="!enabledEmailField" type="button" class="edit" @click="enabledEmailField = true">
        {{ t("settings.button-edit-label") }}
      </button>
    </div>
    <div v-if="showPasswordField">
      <div id="new_password_container" class="stroke password">
        <div class="left">
          <h2>{{ t("settings.new-password-label") }}</h2>
          <input type="password" class="input">
        </div>
      </div>
      <div id="confirm_password_container" class="stroke password">
        <div class="left">
          <h2>{{ t("settings.confirm-password-label") }}</h2>
          <input type="password" class="input">
        </div>
      </div>
    </div>

    <div v-if="showPasswordField || enabledEmailField">
      <div id="current_password_container" class="stroke password">
        <div class="left">
          <h2>{{ t("settings.current-password-label") }}</h2>
          <input type="password" class="input">
        </div>
      </div>
    </div>
    <button
      v-if="!showPasswordField" id="button_change_password" type="button" class="change_password"
      @click="showPasswordField = true"
    >
      {{ t("settings.button-change-password-label") }}
    </button>

    <button v-if="showPasswordField || enabledEmailField" id="edit_account_settings" class="edit account">
      {{ t("settings.button-submit-changes-label") }}
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
    margin: 1% 0%;

    .left {
      h2 {
        font-family: "ClearSans-Medium";
        font-size: 15px;
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
  }

  .edit.account {
    display: flex;
  }

  .input {
    background-color: #303d67;
    border: 0px;
    color: white;
    font-family: "ClearSans-Light";
    font-size: 18px;
    border: 2px #303d67;
    margin-top: 2%;
    width: auto;

    &:disabled {
      background-color: #465586;
      border: 0px;
      color: white;
      font-family: "ClearSans-Light";
      font-size: 18px;
    }

    &:focus {
      background-color: #303d67;
      border: 0px;
      color: white;
      font-family: "ClearSans-Light";
      font-size: 18px;
      outline: 2px solid rgba(39, 55, 91);
    }

    &:-webkit-autofill {
      -webkit-box-shadow: inset 0 0 0 50px #223153;
      /* цвет вашего фона */
      -webkit-text-fill-color: white;
      /* цвет текста */
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
  background-color: #9e6dee;
  font-family: "ClearSans-Light";
  font-size: 18px;
  padding: 1% 3%;
  margin: 1% 0% 2%;
}
</style>
