<script setup lang="ts">
const emit = defineEmits<{
  (e: 'closePopup'): void
}>()
</script>

<template>
  <div class="overlay" @click.self="emit('closePopup')">
    <section class="container">
      <button class="close" @click="emit('closePopup')">
        &times;
      </button>

      <slot />
    </section>
  </div>
</template>

<style lang="scss">
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  background: rgba(0, 0, 0, 0.7);
  transition: opacity 500ms;
  z-index: 10;

  display: flex;
  justify-content: center;
  align-items: center;

  .container {
    position: relative;
    background-color: #303d67;
    border-radius: 10px;
    padding: 50px 50px 30px 50px;

    .close {
      position: absolute;
      font-size: 50px;
      top: -15px;
      right: 10px;
      color: white;
      transition-duration: 0.2s;

      &:hover {
        opacity: 0.7;
      }
    }

    header {
      display: flex;
      justify-content: center;
      align-items: center;
      margin-bottom: 20px;

      h3 {
        font-size: 32px;

        &.warning {
          color: #ff4f4f;
        }
      }
    }

    p {
      font-size: 20px;
    }

    .button-container {
      display: flex;
      justify-content: center;
      align-items: center;
      margin-top: 20px;

      button {
        padding: 6px 24px;
        font-size: 16px;
        margin: 0 10px;
        border-radius: 10px;
        background-color: var(--user-color);
        color: var(--user-contrasting-color);
        transition-duration: 0.2s;

        &:hover {
          opacity: 0.8;
        }
      }
    }

    .confirm-password-container {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 50px;
      margin: 10px 0;

      p {
        font-size: 16px;
      }

      .input {
        background-color: #223153;
        border: 0px;
        color: white;
        font-size: 20px;
        width: auto;
        padding: 6px 12px;
        border-radius: 5px;

        &:focus {
          outline: none;
        }

        &:-webkit-autofill {
          box-shadow: inset 0 0 0 50px #223153;
          -webkit-box-shadow: inset 0 0 0 50px #223153;
          -webkit-text-fill-color: white;
        }
      }
    }

    .image-preview-container {
      display: flex;
      align-items: center;
      justify-content: center;

      img {
        width: auto;
        height: 25vh;
        aspect-ratio: 1 / 1;
        object-fit: cover;
        border-radius: 20px;
      }
    }

    .file-browser-container {
      background-color: #223153;
      width: 800px;
      height: 7vh;
      padding: 1%;
      margin-top: 6px;
      border-radius: 10px;
      position: relative;
      cursor: pointer;
      overflow: hidden;
      vertical-align: middle;
      text-align: left;
      display: flex;

      .file-browser-label {
        display: flex;
        align-items: center;
        background-color: #223153;
        float: left;
        height: auto;
        overflow: hidden;
        padding: 1%;
        font-size: 16px;
        width: 100%;
      }

      .file-browser-button {
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: var(--user-color);
        border-radius: 5px;
        color: var(--user-contrasting-color);
        // float: right;
        font-size: 18px;
        height: auto;
        padding: 3%;
        width: 15%;
      }

      input {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        -moz-opacity: 0;
        filter: alpha(opacity=0);
        opacity: 0;
        height: 100%;
        z-index: 20;
        padding: 0;
        margin: 0;
        cursor: pointer;
      }
    }
  }
}
</style>
