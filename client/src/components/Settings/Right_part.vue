<script setup lang="ts">
import Pages from '~/constants/types/pages'

const { t } = useI18n()

const emit = defineEmits<{
  (e: 'changePage', page: any): void
}>()
</script>

<template>
  <h1>{{ t("settings.button-right-part-header") }}</h1>
  <SideButton text="My Account" icon="carbon:user" @button-click="emit('changePage', Pages.MyAccountPage)" />
  <SideButton text="User Profile" icon="carbon:edit" @button-click="emit('changePage', Pages.UserProfilePage)"/>
  <SideButton text="API Token" icon="carbon:api" @button-click="emit('changePage', Pages.APITokenPage)" />
  <button onclick="location.href='{{ url_for('webapp.index.index_view') }}'" class="standart_button">
    <i class="fi fi-rr-sign-out" />{{ t("settings.button-right-part-back") }}
  </button>
</template>

<style scoped lang="scss">
@import "../../assets/scss/StandartButton.scss";
.standart_button{
  @include standart_buttons;
}

h1{
  margin-bottom: 5%;
}
</style>
