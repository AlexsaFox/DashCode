<script setup lang="ts">
defineProps<{
  label: string
  type: string
  name: string
}>()
</script>

<template>
  <div class="input-container">
    <label :for="name">{{ label }}</label>
    <input :name="name" :type="type">
  </div>
</template>

<style scoped lang="scss">
.input-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
  margin-bottom: 12px;

  label {
    font-family: 'ClearSans-Regular';
    color: #fff;
    font-size: 28px;
  }

  input {
    width: 100%;
    height: 42px;
    padding: 0 8px;
    border-radius: 10px;
    color: white;
    font-family: 'ClearSans-Medium';
    font-size: 18px;
    background-color: #303D67;

    &:focus {
      outline: none;
      background-color: #465586;
    }

    &:-webkit-autofill {
      -webkit-box-shadow: inset 0 0 0 50px #223153;
      /* цвет вашего фона */
      -webkit-text-fill-color: white;
      /* цвет текста */
    }
  }
}
</style>
