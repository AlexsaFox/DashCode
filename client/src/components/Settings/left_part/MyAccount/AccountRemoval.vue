<script setup lang="ts">
const { t } = useI18n()

const showDeleteAccountPopup = ref(false)
</script>

<template>
  <div class="base_settings">
    <div class="account_removal">
      <div class="text">
        <h3>{{ t("settings.account_removal.header") }}</h3>
        <span>{{ t("settings.account_removal.text") }}</span>
      </div>

      <button class="delete_account" @click="showDeleteAccountPopup = true">
        {{ t("settings.account_removal.button-label") }}
      </button>
      <DeleteAccountPopup v-if="showDeleteAccountPopup" @close-popup="showDeleteAccountPopup = false"/>
    </div>
  </div>
</template>

<style scoped lang="scss">
.account_removal {
  display: flex;
  gap: 15%;
  align-items: center;

  .text {
    width: 60%;
    color: rgba(255, 255, 255, 0.6);
    font-weight: 100;
    font-size: 20px;

    h3 {
      font-family: "ClearSans-Medium";
    }

    span {
      font-family: "ClearSans-Regular";
    }
  }

  .delete_account {
    border-radius: 5px;
    background-color: #fa3b3b;
    color: white;
    padding: 1% 2%;
    font-family: "ClearSans-Regular";
    font-size: 20px;
    font-weight: 200;
    width: 20%;
    height: 7vh;
    transition: 0.5s;

    &:hover{
      background-color: #e33030;
      transition: 0.5s;
    }
  }
}
</style>
