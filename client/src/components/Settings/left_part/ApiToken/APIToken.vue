<script setup lang="ts">
const { t } = useI18n()
</script>

<template>
  <div id="APItoken" class="tabcontent">
    <h1>{{ t("settings.api-token-header") }}</h1>
    <hr>
    <div class="API_base">
      <div class="left">
        <h3>{{ t("settings.token-label") }}</h3>
        <textarea id="API_token" class="token" readonly>user.api_token</textarea>
        <button type="button" class="copy_token" onclick="copyToken(event)">
          {{ t("settings.button-copy-token-label") }}
        </button>
      </div>
      <div class="right">
        <h3>{{ t("settings.expiration-datetime-label") }}</h3>
        <span> api_token_expiration_datetime</span>
        <form action="{{ url_for('webapp.user.settings.regenerate_api_token') }}" method="post">
          <button type="submit" class="generate_token">
            {{ t("settings.button-generate-new-token-label") }}
          </button>
        </form>
      </div>
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
  }

}

/*
нижняя строчка с настройками по смене пароля и удалению аккуанта
*/

.tabcontent hr {
  margin-top: 3%;
  border: 0px;
  border-top: 3px solid #465586;
}

.vertical {
  border-left: 3px solid #465586;
  height: 150px;
  width: 1px;
}

.API_base {
  display: flex;
  justify-content: space-between;
  padding-bottom: 2%;
  margin-top: 3%;

  .left {
    width: 45%;
    display: block;
    height: auto;

    .token {
      width: 50%;
      border: 0px;
      display: block;
      background-color: #303D67;
      color: white;
      border-radius: 10px;
      font-family: 'ClearSans-Medium';
      font-size: 18px;
      padding: 3%;
      resize: none;
      width: 100%;
      height: 175px;
    }

    .token:focus {
      outline: none;
    }

    .copy_token {
      margin: 4% 0% 0%;
      background-color: #465586;
      width: 100%;
      height: 7vh;
      font-family: 'ClearSans-Medium';
      color: white;
      font-size: 20px;
      padding: 1%;
      border-radius: 10px;
      border: 0;
      transition: 0.5s;
    }

    .copy_token:hover {
      background-color: #303D67;
      cursor: pointer;
      transition: 0.5s;
    }
  }

  .right {
    width: 45%;
    display: block;
    height: auto;

    span {
      color: white;
      font-family: 'ClearSans-Medium';
      font-size: 20px;
      font-weight: 200;
    }

    .generate_token {
      background-color: #465586;
      bottom: 0px;
      margin-top: 15%;
      width: 80%;
      height: 60px;
      border-radius: 10px;
      color: white;
      font-family: 'ClearSans-Medium';
      font-size: 18px;
      border: 0;
      transition: 0.5s;
    }

    .generate_token:hover {
      background-color: #303D67;
      cursor: pointer;
      transition: 0.5s;
    }
  }
}
</style>
