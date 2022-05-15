<script setup lang="ts">
import useAuthStore from '~/store/useAuth'
import useErrorsStore from '~/store/useErrors'

const { t } = useI18n()
const router = useRouter()

const emit = defineEmits<{
  (e: 'closePopup'): void
}>()

const fileForm = ref<HTMLInputElement | null>(null)
const imageData = ref('')
const imageName = ref('')

function updatePreviewImage() {
  const files = fileForm.value?.files
  if (files) {
    imageName.value = files[0].name
    const fileReader = new FileReader()
    fileReader.readAsDataURL(files[0])
    fileReader.onload = function() {
      const result = this.result
      if (result instanceof ArrayBuffer)
        imageData.value = result.toString()
      else
        imageData.value = result ?? ''
    }
  }
}

function onSubmit() {
  const files = fileForm.value?.files
  if (files) {
    useAuthStore().editProfilePicture(files[0]).then(() => {
      if (useErrorsStore().errors.length === 0)
        router.go(0)
    })
  }
  else { emit('closePopup') }
}
</script>

<template>
  <div class="overlay">
    <div class="popup">
      <div class="header">
        <span>{{ t("settings.button-edit-avatar-label") }}</span>
        <button class="close" @click="emit('closePopup')">
          &times;
        </button>
      </div>
      <div class="content">
        <img v-if="imageData" :src="imageData">
        <div class="field">
          <span class="label">{{ t("settings.upload-profile-image-label") }}</span>
          <div class="fileform">
            <div id="fileformlabel">
              {{ imageName }}
            </div>
            <div class="selectbutton">
              {{ t("settings.button-browse-image-label") }}
            </div>
            <input
              id="id_profile_picture" ref="fileForm" type="file" name="profile_picture"
              @change="updatePreviewImage"
            >
          </div>
        </div>

        <div class="send-button-container">
          <button type="submit" class="send_button" @click="onSubmit">
            {{ t("settings.button-submit-changes-label") }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.overlay {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7);
  transition: opacity 500ms;
  height: 100%;
  z-index: 10;
  overflow-y: auto;
}

.popup {
  margin: 70px auto;
  background: #303d67;
  border-radius: 10px;
  width: 50%;
  position: relative;
  padding: 2%;

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .close {
    transition: all 200ms;
    font-size: 50px;
    text-decoration: none;
    color: white;

    &:hover {
      color: #465586;
    }

  }

  span {
    font-family: 'ClearSans-Medium';
    color: rgba(255, 255, 255, 0.8);
    font-size: 24px;
  }

  .content {
    text-align: left;
    font-family: 'ClearSans-Regular';
    color: white;
    padding: 0px 3%;
    max-height: 40%;
    overflow: auto;
    background-color: #303d67;
    border-radius: 0 0 10px 10px;
    display: flex;
    flex-direction: column;
    align-items: center;

    img {
      width: auto;
      height: 25vh;
      aspect-ratio: 1 / 1;
      border-radius: 20px;
    }

    .send-button-container {
      width: 100%;
      text-align: center;
    }

    .field {
      margin-top: 12px;
      width: 100%;

      .label {
        font-family: "ClearSans-Medium";
        color: rgba(255, 255, 255, 0.6);
        font-size: 20px;
      }
    }

    .send_button {
      font-family: "ClearSans-Regular";
      color: white;
      margin: auto;
      margin-top: 3%;
      padding: 6px 12px;
      background: #223153;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      font-size: 20px;
      transition-duration: 0.2s;

      &:hover {
        background: #303d67;
      }

      &:disabled {
        opacity: 0.6;
      }

      &:disabled:hover {
        background: #465586;
      }
    }
  }
}

.fileform {
  background-color: #223153;
  width: 100%;
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

  #fileformlabel {
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

  .selectbutton {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #9e6dee;
    border-radius: 5px;
    color: #223153;
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
</style>
