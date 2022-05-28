<script setup lang="ts">
import { onBeforeRouteLeave } from 'vue-router'
import noteEditActions from '~/constants/types/noteEditActions'
import useAuthStore from '~/store/useAuth'
import useErrors from '~/store/useErrors'
import { getTagColor } from '~/utils/colors'
import renderMarkdown from '~/utils/renderMarkdown'

const errors = useErrors()
const router = useRouter()
const { t } = useI18n()

interface Props {
  title?: string
  isPrivate?: boolean
  content?: string
  tags?: string[]
  link?: string
  saveAction: (title: string, isPrivate: boolean, content: string, tags: string[], link?: string) => void
}

const {
  title = '',
  isPrivate = true,
  content = '',
  tags = [],
  link = '',
  saveAction,
} = defineProps<Props>()
const note = ref({
  title,
  isPrivate,
  content,
  tags,
  link,
})

const privacySelectorValue = ref(isPrivate ? 'private' : 'public')

const newTag = ref('')
function addTag() {
  if (newTag.value.length === 0)
    return

  if (note.value.tags.includes(newTag.value))
    removeTag(newTag.value)

  note.value.tags.push(newTag.value)
  newTag.value = ''
}
function removeTag(removedTag: string) {
  note.value.tags = note.value.tags.filter(tag => tag !== removedTag)
}
function sanitizeNewTagInput() {
  let sanitized = ''
  for (let i = 0; i < newTag.value.length; i++) {
    const letterCode = newTag.value.charCodeAt(i)
    if ((letterCode >= 97 && letterCode <= 122) // a-z
      || (letterCode >= 48 && letterCode <= 57) // 0-9
      || (letterCode === 45)) // - (dash symbol)
      sanitized += newTag.value[i]
    else if (letterCode >= 65 && letterCode <= 90) // A-Z => a-z
      sanitized += newTag.value[i].toLowerCase()
    else if (letterCode === 32 || letterCode === 95) // ' ', '_' => '-'
      sanitized += '-'
  }
  newTag.value = sanitized
}

const markdownShown = ref(false)
const markdownHTML = ref('')
const contentTextarea = ref<null | HTMLTextAreaElement>(null)
function handleTabPress() {
  if (contentTextarea.value !== null) {
    const cursorPos = contentTextarea.value.selectionStart
    const before = note.value.content.substring(0, cursorPos)
    const after = note.value.content.substring(cursorPos)
    note.value.content = `${before}    ${after}`
    nextTick(() => {
      if (contentTextarea.value !== null)
        contentTextarea.value.setSelectionRange(cursorPos + 4, cursorPos + 4)
    })
  }
}
function handleBackspacePress(event: KeyboardEvent) {
  if (contentTextarea.value !== null) {
    const cursorPos = contentTextarea.value.selectionStart
    const before = note.value.content.substring(0, cursorPos - 4)
    const previousFour = note.value.content.substring(cursorPos - 4, cursorPos)
    const after = note.value.content.substring(cursorPos)
    if (previousFour === '    ') {
      note.value.content = `${before}${after}`
      event.preventDefault()
      nextTick(() => {
        if (contentTextarea.value !== null)
          contentTextarea.value.setSelectionRange(cursorPos - 4, cursorPos - 4)
      })
    }
  }
}
function changeShowMarkdown() {
  markdownShown.value = !markdownShown.value
  if (markdownShown.value)
    markdownHTML.value = renderMarkdown(note.value.content)
}

const showConfirmPopup = ref(false)
let nextRoute = null as null | string
function handleExitAction(action: noteEditActions) {
  showConfirmPopup.value = false

  if (action === noteEditActions.discard) {
    if (nextRoute !== null)
      router.push(nextRoute)
  }

  else if (action === noteEditActions.save) {
    saveNote()
    if (nextRoute !== null && errors.errors.length === 1)
      router.push(nextRoute)
  }

  else if (action === noteEditActions.cancel) { nextRoute = null }
}

let savingNote = false
function saveNote() {
  savingNote = true
  saveAction(
    note.value.title,
    privacySelectorValue.value === 'private',
    note.value.content,
    note.value.tags,
    note.value.link,
  )
}

onBeforeRouteLeave((to) => {
  if (!useAuthStore().loggedIn || savingNote)
    return true

  if (nextRoute !== null)
    return true

  showConfirmPopup.value = true
  nextRoute = to.path
  return false
})
</script>

<template>
  <Transition name="modal">
    <PopupCheck v-if="showConfirmPopup" @action="(action) => handleExitAction(action)" />
  </Transition>

  <div class="crutch">
    <section class="main-container">
      <section class="close-bar">
        <button @click="router.back()">
          <div class="i-carbon:close" />
        </button>
      </section>

      <section class="title-bar">
        <input v-model="note.title" :placeholder="t('note.attributes.title')">
        <select v-model="privacySelectorValue">
          <option value="private">
            {{ t('note.attributes.privacy.private') }}
          </option>
          <option value="public">
            {{ t('note.attributes.privacy.public') }}
          </option>
        </select>
      </section>

      <section class="content-bar">
        <textarea
          v-if="!markdownShown"
          ref="contentTextarea"
          v-model="note.content"
          :placeholder="t('note-edit.content.placeholder')"
          @keydown.tab.prevent="handleTabPress"
          @keydown.delete="handleBackspacePress"
        />
        <div v-else class="markdown" readonly v-html="markdownHTML" />
        <div class="button-container">
          <button @click="changeShowMarkdown">
            {{ markdownShown ? t('note-edit.unpreview-markdown') : t('note-edit.preview-markdown') }}
          </button>
        </div>
      </section>

      <section class="tag-bar">
        <ul>
          <li
            v-for="tag in note.tags"
            :key="tag"
            class="clickable"
            :style="`background-color: ${getTagColor(tag)};`" @click="removeTag(tag)"
          >
            {{ tag }}
          </li>
          <li class="add-tag">
            <input
              v-model="newTag" maxlength="30" placeholder="new tag" :size="newTag.length + 1"
              @input="sanitizeNewTagInput"
            >
            <button @click="addTag">
              Add
            </button>
          </li>
        </ul>
      </section>

      <section class="link-bar">
        <input v-model="note.link" placeholder="https://example.com">
        <button @click="saveNote">
          {{ t('note-edit.save-button') }}
        </button>
      </section>
    </section>
  </div>
</template>

<style scoped lang="scss">
@import '/src/components/Modal/modal-transition.scss';
@import './note-preview.scss';
</style>
