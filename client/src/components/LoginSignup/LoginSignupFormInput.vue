<script setup lang="ts">
defineProps<{
  label: string
  type: string
}>()

const emit = defineEmits<{
  (e: 'changed', newValue: string): void
}>()

const inputValue = ref('')
</script>

<template>
  <div class="input-container">
    <label :for="label">{{ label }}</label>
    <input v-model="inputValue" :name="label" :type="type" @change="emit('changed', inputValue)">
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
  }
}
</style>
