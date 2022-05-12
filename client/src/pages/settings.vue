<script setup lang="ts">

enum Pages{
  MyAccountPage,
  UserProfilePage,
  APITokenPage,
}

const activePage = ref(Pages.MyAccountPage)

</script>

<template>
  <div class="page_settings">
    <div class="left_part">
      <MyAccount v-if="activePage == Pages.MyAccountPage" />
      <UserProfile v-if="activePage == Pages.UserProfilePage" />
      <APIToken v-if="activePage == Pages.APITokenPage" />
    </div>
    <div class="right_part">
      <Right_part @change-page="(page) => { activePage = page}" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.page_settings {
    background-color: #1A2641;
    display: flex;
    justify-content: space-between;
    padding: 2%;
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
    right: 2%;
    top: 1%;
}
</style>
