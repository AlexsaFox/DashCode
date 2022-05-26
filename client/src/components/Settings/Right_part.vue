<script setup lang="ts">
import Pages from '~/constants/types/pages'
import useSettingsPageStore from '~/store/useSettingsPage'

const { t } = useI18n()
const router = useRouter()
const settingsPage = useSettingsPageStore()
</script>

<template>
  <h1>{{ t("settings.button-right-part-header") }}</h1>
  <SideButton icon="" @button-click="settingsPage.changePage(Pages.MyAccountPage)">
    <span class="i-carbon-user" /> {{ t('settings.button-right-part-account') }}
  </SideButton>
  <SideButton @button-click="settingsPage.changePage(Pages.UserProfilePage)">
    <span class="i-carbon-edit" />  {{ t('settings.button-right-part-profile') }}
  </SideButton>
  <SideButton @button-click="settingsPage.changePage(Pages.APITokenPage)">
    <span class="i-carbon-api" />  {{ t('settings.button-right-part-token') }}
  </SideButton>
  <SideButton @button-click="router.back()">
    <span class="i-carbon:arrow-left" />{{ t("settings.button-right-part-back") }}
  </SideButton>
</template>

<style scoped lang="scss">
@import "../../assets/scss/standard-button.scss";
.standard-button{
  @include standard-button;
}

h1{
  margin-bottom: 5%;
}
</style>
