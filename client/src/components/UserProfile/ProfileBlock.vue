<script setup lang="ts">
import useAuthStore from '~/store/useAuth'

const auth = useAuthStore()
</script>
<template>
  <div class="profile_block">
    <div class="avatar">
      <img :src="auth.profilePicture" class="avatar" alt="Avatar">
    </div>
    <div class="text">
      <span>@Anonim</span>
    </div>
    <div class="amount_of_notes">
      <span>public notes: 20</span>
    </div>
  </div>
</template>
<style scoped lang="scss">
  .profile_block {
    display: inline-block;
    padding: 1.5%;
    background-color: #223153;
    text-align: center;
    width:60%;
    margin-top: 5%;
    margin-left: 10%;
    border-radius: 10px;
    color:white;
    font-family: 'ClearSans-Regular';
    .text{
      display: block;
      margin-bottom: 0.5%;
    }
    .amount_of_notes span {
      font-size: 20px;
    }
    .text span{
      font-size: 24px;
    }
    .amount_of_notes{
       display:block;
       margin-left: 2%;

    }
    .avatar{
      display:block;
      margin-left: auto;
      margin-right: auto;
    }
    img {
      padding: 5px;
      border-radius: 50%;
      width: 125px;
      height: 125px;
      object-fit: cover;
    }
  }
</style>
