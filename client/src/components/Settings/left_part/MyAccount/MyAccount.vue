<script setup lang="ts">
const { t } = useI18n()
</script>

<template>
  <div id="MyAccount" class="tabcontent">
    <h1>{{ t("settings.my-account-header") }}</h1>
    <hr>
    <h3>{{ t("settings.my-account-header-base-settings") }}</h3>
    <AccountPreview />
    <hr>
    <AccountRemoval />
  </div>
</template>

<style scoped lang="scss">
.profile h2 {
  font-family: "ClearSans-Bold";
  color: white;
  margin: 0%;
}
.tabcontent {
  // display: none;
  background-color: #223153;
  border-radius: 15px;
  padding: 3%;
  h1 {
    font-family: "ClearSans-Bold";
    font-size: 28px;
    margin-bottom: 2%;
  }
  h3 {
    font-family: "ClearSans-Medium";
    color: rgba(255, 255, 255, 0.6);
    font-weight: 100;
    margin-bottom: 2%;
  }

}

/*
нижняя строчка с настройками по смене пароля и удалению аккуанта
*/

.tabcontent hr {
  margin-top: 3%;
  margin-bottom: 2%;
  border: 0px;
  border-top: 3px solid #465586;
}

.vertical {
  border-left: 3px solid #465586;
  height: 150px;
  width: 1px;
}
</style>
