<template>
  <div class="stroke">
    <div class="profile">
      <div class="avatar_s">
        <img
          src="src/assets/img/2e483781-a491-4b82-9bf4-560a76752829.jpg"
        >
      </div>
      <h2>USERNAME</h2>
    </div>
    <button
      type="button"
      class="edit_profile"
      onclick="openSettings(event, 'UserProfile')"
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
    gap: 10%;
    width: 30%;
  }
  .stroke.username {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: auto;
    margin: 3% 2% 3% 4%;
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
  }
  .edit_profile:hover {
    cursor: pointer;
    opacity: 0.8;
  }
  .stroke_s {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 8%;
    width: auto;
    margin: -3% 0% 2% 4%;
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
}
</style>
