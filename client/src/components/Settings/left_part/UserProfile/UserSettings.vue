<script setup lang="ts">
// const { t } = useI18n()

</script>
<template>
  <div class="account_preveiw">
    <div class="profile_color" />
    <div class="stroke_s">
      <div class="profile">
        <a href="#popup_avatar">
          <div class="avatar_s">
            <img src="src/assets/img/2e483781-a491-4b82-9bf4-560a76752829.jpg">
          </div>
        </a>
        <EditAvatarPopup />
      </div>
    </div>
    <ChangeUsername />
  </div>
</template>

<style scoped lang="scss">
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
  background-color: #9e6dee;
  width: 50%;
  height: 35px;
  border: 0px;
  border-radius: 5px;
  color: #223153;
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
  width: 5vw;
  height: 10vh;
  display: inline-block;

  img {
    border-radius: 50%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 5vw;
    height: 10vh;
    display: inline-block;
    object-fit: cover;
  }
}

.account_preveiw {
  border-radius: 15px;
  background-color: #303d67;
  padding-bottom: 2%;
  margin-right: 40%;

  .profile_color {
    background-color: #9e6dee;
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
