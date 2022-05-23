<script setup lang="ts">
const { t } = useI18n()
</script>

<template>
  <div id="UserProfile" class="tabcontent">
    <h1>{{ t('settings.user-profile.header.label') }}</h1>
    <hr>
    <div class="user_stroke">
      <h3>{{ t('settings.user-profile.header.preview') }}</h3>
      <div class="first_block">
        <UserSettings />
      </div>
    </div>
    <hr>

    <div class="bottom_line">
      <ChangeColor />
      <ChangeLanguage />
    </div>
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
    margin: 0%;
    font-size: 28px;
    margin-bottom: 2%;
  }

  h3 {
    font-family: "ClearSans-Medium";
    color: rgba(255, 255, 255, 0.6);
    font-weight: 100;
    margin-bottom: 2%;
    font-size: 20px;
  }

  .first_block {
    display: flex;
    justify-content: center;
  }

  .bottom_line {
    display: flex;
  }

}

/*
нижняя строчка с настройками по смене пароля и удалению аккуанта
*/

.tabcontent hr {
  margin: 3% 0% 2%;
  border: 0px;
  border-top: 3px solid #465586;
}

.vertical {
  border-left: 3px solid #465586;
  height: 150px;
  width: 1px;
}
</style>
