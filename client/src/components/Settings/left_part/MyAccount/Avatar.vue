<script setup lang="ts">
import useAuthStore from '~/store/useAuth'
import useSettingsPageStore from '~/store/useSettingsPage'
import Pages from '~/constants/types/pages'

const auth = useAuthStore()
const settingsPage = useSettingsPageStore()
</script>

<template>
  <div class="stroke">
    <div class="profile">
      <div class="avatar_s">
        <user-profile-picture />
      </div>
      <h2>{{ auth.user.username }}</h2>
    </div>
    <button
      type="button"
      class="edit_profile"
      @click="settingsPage.changePage(Pages.UserProfilePage)"
    >
      Edit User Profile
    </button>
  </div>
</template>

<style scoped lang="scss">
.stroke {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: auto;
  margin: -1% 2% 3% 3%;

  .profile {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    width: 30%;

    h2{
      font-family: 'ClearSans-Regular';
      font-size: 24px;
    }
  }
  .stroke.username {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: auto;
    margin: 3% 2% 3% 4%;
  }
  .edit_profile {
    background-color: var(--user-color);
    width: 50%;
    height: 35px;
    border: 0px;
    border-radius: 5px;
    color: var(--user-contrasting-color);
    font-family: "ClearSans-Light";
    font-size: 18px;
    transition: 0.5s;
  }
  .edit_profile:hover {
    cursor: pointer;
    opacity: 0.8;
  }
  .avatar_s {
    overflow: hidden;
    height: 120px;
    width: 120px;
    min-width: 120px;
    border-radius: 100%;

    border: 10px solid #303d67;

    img {
      height: 100%;
      width: 100%;
      object-fit: cover;
    }
  }
}
</style>
