<script setup lang="ts">
defineProps<{
  bottomText: string
  bottomLinkText: string
  bottomLinkRoute: string
  submitButtonText: string
  submitAction: () => void
}>()
</script>

<template>
  <div class="form-container">
    <form>
      <slot />
      <button @click.prevent="submitAction()">
        {{ submitButtonText }}
      </button>
    </form>
    <p>
      {{ bottomText }} <router-link :to="bottomLinkRoute">
        {{ bottomLinkText }}
      </router-link>
    </p>
  </div>
</template>

<style scoped lang="scss">
@import './blockparts.scss';

.form-container {
  @include block-part;

  form {
    width: 100%;
    border-radius: 20px;
    background-color: #ffffff3f;
    padding: 20px;

    button {
      width: 100%;
      padding: 6px 0;
      margin-top: 12px;
      border-radius: 10px;
      color: #223153;
      font-size: 24px;
      font-family: 'ClearSans-Bold';
      font-weight: bold;
      text-align: center;
      background-color: #9e6dee;
    }
  }

  p {
    margin: 10px;
    color: white;
    font-size: 20px;
    font-family: 'ClearSans-Regular';

    a {
      color: #9e6dee;
    }
  }
}
</style>
