<script setup lang="ts">
const { t } = useI18n()

const editUsernameField = ref(false)
</script>

<template>
  <div class="stroke username">
    <div class="edit_username">
      <div class="left">
        <h2>{{ t("settings.username-label") }}</h2>
        <input :disabled="!editUsernameField" class="input username" value="Username">
      </div>
    </div>
    <button v-if="!editUsernameField" type="button" class="edit username" @click="editUsernameField = true">
      {{ t("settings.button-edit-label") }}
    </button>
    <button v-if="editUsernameField" class="edit name">
      {{ t("settings.button-submit-changes-label") }}
    </button>
  </div>
</template>

<style scoped lang="scss">
.edit_username {
  display: flex;

  h2 {
    font-family: "ClearSans-Medium";
    font-size: 15px;
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
  font-size: 18px;
  border: 2px #303d67;
  margin-top: 2%;
  width: auto;

  &:disabled {
    background-color: #303d67;
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

  & :-webkit-autofill {
    -webkit-box-shadow: inset 0 0 0 50px #223153;
    /* цвет вашего фона */
    -webkit-text-fill-color: white;
    /* цвет текста */
  }
}
</style>
