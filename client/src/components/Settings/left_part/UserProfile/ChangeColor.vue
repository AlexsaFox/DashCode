<script setup lang="ts">
const { t } = useI18n()
</script>

<template>
  <div class="first_block profile_color">
    <h4>{{ t("settings.change-color-label") }}</h4>
    <div class="bottom_line">
      <input type="color" class="change_profile_color">
      <button class="edit">
        {{ t("settings.button-edit-label") }}
      </button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.first_block.profile_color {
  .bottom_line {
    display: flex;
    justify-content: flex-start;
    gap: 5%;
    align-items: center;
    width: 50%;
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
      width: 16%;
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
