<script setup lang="ts">
import useSettingsPageStore from '~/store/useSettingsPage'
import Pages from '~/constants/types/pages'

const settingsPage = useSettingsPageStore()
settingsPage.changePage(Pages.MyAccountPage)
</script>

<template>
  <div class="page_settings">
    <div class="left_part">
      <MyAccount v-if="settingsPage.currentPage == Pages.MyAccountPage" />
      <UserProfile v-if="settingsPage.currentPage == Pages.UserProfilePage" />
      <APIToken v-if="settingsPage.currentPage == Pages.APITokenPage" />
    </div>
    <div class="right_part">
      <Right_part />
    </div>
  </div>
</template>

<style scoped lang="scss">
.page_settings {
    background-color: #1A2641;
    display: flex;
    justify-content: space-between;
    padding: 15px;
    color: white;
    width: auto;
}

.left_part {
    width: 75%;
}
.right_part {
    width: 20%;
    display: flex;
    flex-direction: column;
    font-family: 'ClearSans-Bold';
    font-size: 32px;
    position: fixed;
    right: 15px;
    top: 1%;
}
</style>
