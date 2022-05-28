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
  <modal @close-popup="emit('closePopup')">
    <header>
      <h3>{{ t("settings.button.edit.avatar-label") }}</h3>
    </header>

    <div class="image-preview-container">
      <img v-if="imageData" :src="imageData">
    </div>

    <p>{{ t("settings.upload-profile-image-label") }}</p>

    <div class="file-browser-container">
      <div class="file-browser-label">
        {{ imageName }}
      </div>
      <div class="file-browser-button">
        {{ t("settings.button.browse-image-label") }}
      </div>
      <input
        ref="fileForm" type="file" name="profile_picture"
        @change="updatePreviewImage"
      >
    </div>

    <div class="button-container">
      <button type="submit" @click="onSubmit">
        {{ t("settings.button.submit.changes-label") }}
      </button>
    </div>
  </modal>
</template>
