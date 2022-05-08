<script setup lang="ts">
import useErrorsStore from '~/store/useErrors'

const errors = useErrorsStore()
</script>

<template>
  <section>
    <ul>
      <li v-for="error in errors.errors" :key="error">
        <p>{{ error }}</p>
        <button class="icon-btn mx-2" @click="errors.removeError(error)">
          <div i-carbon:close />
        </button>
      </li>
    </ul>
  </section>
</template>

<style scoped lang="scss">
@keyframes error-fade-in {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}
section {
  position: fixed;

  ul {
    padding: 0 10px;
    width: 100vw;

    li {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      margin: 10px 0;
      padding: 10px;
      border-radius: 10px;

      color: #400;
      background-color: #f88;
      animation: error-fade-in 0.3s;

      p {
        font-family: "ClearSans-Regular";
        font-size: 16px;
      }

      button {
        font-size: 28px;

        &:hover {
          color: #800;
        }
      }
    }
  }
}
</style>
