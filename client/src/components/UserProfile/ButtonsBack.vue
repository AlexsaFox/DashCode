<script setup lang="ts">
const { t } = useI18n()
</script>
<template>
  <div class="block">
    <div class="display_with_button">
      <a><button class="standard_button">
        <div class="i-carbon:arrow-right" />{{ t("user-profile.buttons-back.button-back-to-profile") }}
      </button></a>
      <a><button class="standard_button">
        <div class="i-carbon:user-avatar-filled-alt" />{{ t("user-profile.buttons-back.button-back-to-social-media") }}
      </button></a>
    </div>
  </div>
</template>
<style scoped lang="scss">
@import "../../assets/scss/standard-button.scss";

.standard_button {
  @include standard-button;
}
.block {
  color: white;
  font-family: 'ClearSans-Regular';
  display: inline-block;
  position: fixed;
  width: 20%;
  right: 15px;
  top: 0px;
}
.b_my_notes:focus {
  background-color: var(--primary-color);
}

.display_with_button {
  display: inline-block;
  width: 100%;
  margin-top: 25%;
  div{
    color: #F1F7ED;
  }
  button{
    width: 100%;
  }
}
</style>
