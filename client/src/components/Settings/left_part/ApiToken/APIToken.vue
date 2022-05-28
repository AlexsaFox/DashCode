<script setup lang="ts">
const { t } = useI18n()

const token = ref('')
const showToken = ref(false)
const showCopySuccess = ref(false)
const showResetTokenPopup = ref(false)

function copyToken() {
  timeoutShowCopySuccess()
}

async function timeoutShowCopySuccess() {
  showCopySuccess.value = true
  await navigator.clipboard.writeText(token.value)
  setTimeout(() => {
    showCopySuccess.value = false
  }, 1500)
}

function renewToken() {
  token.value = localStorage.getItem('token') ?? ''
  showResetTokenPopup.value = false
}
renewToken()
</script>

<template>
  <Transition name="modal">
    <ResetTokenPopup v-if="showResetTokenPopup" @close-popup="renewToken" />
  </Transition>

  <div id="APItoken" class="tabcontent">
    <h1>{{ t("settings.api-token-header") }}</h1>
    <hr>
    <div class="API_base">
      <div class="left">
        <h3>{{ t("settings.token-label") }}</h3>
        <textarea v-if="showToken" id="API_token" v-model="token" class="token shown" readonly />
        <div v-else class="token hidden">
          <p>{{ t('settings.token.token-hidden') }}</p>
        </div>
      </div>
      <div class="right">
        <button type="submit" class="button_token" @click="showToken = !showToken">
          <span v-if="showToken">{{ t("settings.button.hide-token-label") }}</span>
          <span v-else>{{ t("settings.button.show-token-label") }}</span>
        </button>
        <button type="button" :class="'button_token' + (showCopySuccess ? ' copied-success' : '')" @click="copyToken">
          {{ showCopySuccess ? t("settings.token.copied") : t("settings.button.copy-token-label") }}
        </button>
        <button type="button" class="button_token" @click="showResetTokenPopup = true">
          {{ t("settings.button.reset-token-label") }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import '/src/components/Modal/modal-transition.scss';

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

.API_base {
  display: flex;
  justify-content: space-between;
  padding-bottom: 2%;

  .left {
    width: 45%;
    display: block;
    height: auto;

    .token {
      width: 50%;
      border: 0px;
      display: block;
      background-color: #303D67;
      border-radius: 10px;
      font-family: 'ClearSans-Medium';
      font-size: 20px;
      padding: 3%;
      resize: none;
      width: 100%;
      height: 200px;

      &.shown {
        color: white;
      }
      &.hidden {
        display: flex;
        justify-content: center;
        align-items: center;
        color: #ffffff88;
        font-size: 32px
      }

      &:focus {
        outline: none;
      }

    }
  }

  .right {
    width: 45%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: auto;

    span {
      color: white;
      font-family: 'ClearSans-Medium';
      font-size: 20px;
      font-weight: 200;
    }

    @mixin side-blob {
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
    }

    .button_token {
      @include side-blob;
      transition: 0.3s;

      &:hover {
        background-color: #303D67;
        cursor: pointer;
        transition: 0.3s;
      }

      &.copied-success {
        background-color: rgb(96, 179, 69);
      }
    }
  }

}
</style>
