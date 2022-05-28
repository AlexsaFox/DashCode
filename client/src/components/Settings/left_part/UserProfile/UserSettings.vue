<script setup lang="ts">
const showEditAvatarPopup = ref(false)
</script>

<template>
  <div class="account_preveiw">
    <div class="profile_color" />
    <div class="stroke_s">
      <div class="profile">
        <button @click="showEditAvatarPopup = !showEditAvatarPopup">
          <div class="avatar_s">
            <user-profile-picture />
          </div>
        </button>

        <Transition name="modal">
          <EditAvatarPopup v-if="showEditAvatarPopup" @close-popup="showEditAvatarPopup = false" />
        </Transition>
      </div>
    </div>
    <ChangeUsername />
  </div>
</template>

<style scoped lang="scss">
@import '/src/components/Modal/modal-transition.scss';

.user_stroke {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;

  hr {
    margin-top: 5%;
    border: 0px;
    border-top: 3px solid #465586;
  }
}

.edit {
  border-radius: 5px;
  background-color: #223153;
  border: 0px;
  padding: 1% 2%;
  color: white;
  font-family: 'ClearSans-Light';
  font-size: 20px;
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

  &:hover {
    cursor: pointer;
    opacity: 0.8;
  }
}

.avatar_s {
  position: relative;
  overflow: hidden;
  height: 120px;
  width: 120px;
  min-width: 120px;
  border-radius: 100%;

  background-color: #303d67;
  border: 10px solid #303d67;

  img {
    height: 100%;
    width: 100%;
    object-fit: cover;
  }
}

.account_preveiw {
  border-radius: 15px;
  background-color: #303d67;
  padding-bottom: 2%;
  width: 50%;

  .profile_color {
    background-color: var(--user-color);
    height: 90px;
    border-radius: 15px 15px 0px 0px;
  }

  .stroke.username {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: auto;
    margin: 3% 2% 3% 4%;
  }

  .stroke_s {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 8%;
    width: auto;
    margin: -3% 0% 2% 4%;
  }
}
</style>
