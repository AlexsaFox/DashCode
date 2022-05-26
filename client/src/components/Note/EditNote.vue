<script setup lang="ts">
import { onBeforeRouteLeave } from 'vue-router'
import noteEditActions from '~/constants/types/noteEditActions'
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

function saveNote() {
  saveAction(
    note.value.title,
    privacySelectorValue.value === 'private',
    note.value.content,
    note.value.tags,
    note.value.link,
  )
}

onBeforeRouteLeave((to) => {
  if (nextRoute !== null)
    return true

  showConfirmPopup.value = true
  nextRoute = to.path
  return false
})
</script>

<template>
  <PopupCheck v-if="showConfirmPopup" @action="(action) => handleExitAction(action)" />

  <div class="crutch">
    <section class="main-container">
      <section class="close-bar">
        <button @click="router.push('/')">
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
          <li v-for="tag in note.tags" :key="tag" :style="`background-color: ${getTagColor(tag)};`" @click="removeTag(tag)">
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

<style lang="scss">
@import '/src/assets/scss/markdown-config.scss';

.crutch {
  border: 0.1px solid transparent;
}

.main-container {
  padding-top: 8px;
  background-color: #617299;
  width: 70%;
  margin-top: 70px;
  margin-left: 5%;
  border-radius: 10px;

  .close-bar {
    display: flex;
    justify-content: flex-end;
    margin: 0 10px;
    width: calc(100% - 20px);

    button {
      font-size: 230%;
      cursor: pointer;
      color: #F1F7ED;
      transition-duration: 0.2s;

      &:hover {
        transform: scale(1.1);
      }
    }
  }

  .title-bar {
    display: flex;
    justify-content: space-between;
    align-items: stretch;
    gap: 1%;
    padding: 8px 20px 20px 20px;
    font-family: 'ClearSans-Light';
    font-size: 20px;

    input {
      width: 100%;
      padding: 10px;
      border-radius: 10px;
      background-color: rgba(255, 255, 255, 0.1);
      font-size: 20px;
      color: white;

      &:focus {
        outline: none;
      }
    }

    select {
      color: var(--user-contrasting-color);
      background-color: var(--user-color);
      border-radius: 10px;
      width: 14%;
      padding: 4px 0px;
      text-align: center;
      color: white;
      font-size: 18px;

      option {
        color: var(--user-contrasting-color);
        background-color: var(--user-color);
        margin: 5px 0;
        border: none;
      }

      &:focus {
        outline: none;
      }
    }
  }

  .content-bar {
    font-size: 0;

    @mixin content-container {
      font-family: 'ClearSans-Regular';
      border-radius: 10px;
      padding: 10px;
      resize: none;
      width: calc(100% - 40px);
      margin: 0 20px;
      font-size: 16px;
      min-height: 20em;
      resize: vertical;
    }

    textarea {
      @include content-container;
      background-color: rgba(255, 255, 255, 0.1);

      &::-webkit-scrollbar-track {
        background-color: transparent;
      }

      &:focus {
        outline: none;
      }
    }

    .markdown {
      @include content-container;
      @include markdown-config;
    }

    .button-container {
      margin: 10px 20px;
      display: flex;
      justify-content: right;

      button {
        color: var(--user-contrasting-color);
        background-color: var(--user-color);
        padding: 10px 32px;
        border-radius: 10px;
        text-align: right;
        font-size: 18px;
        transition-duration: 0.2s;

        &:hover {
          opacity: 0.8;
        }
      }
    }
  }

  .tag-bar {
    padding: 10px 20px;

    ul {
      display: flex;
      justify-content: baseline;
      flex-wrap: wrap;
      padding: 10px;
      border-radius: 10px;
      background-color: rgba(255, 255, 255, 0.1);
      font-family: 'ClearSans-Regular';

      li {
        margin: 3px 6px;
        padding: 2px 10px;
        border-radius: 10px;

        &:hover {
          cursor: pointer;
        }
      }

      li.add-tag {
        margin: 3px 6px;
        padding: 0;
        overflow: hidden;

        input {
          height: 100%;
          padding: 2px 10px;
          min-width: 100px;
          background-color: rgba(255, 255, 255, 0.1);
          color: white;

          &::placeholder {
            color: #ffffff80;
          }

          &:focus {
            outline: none;
          }
        }

        button {
          color: var(--user-contrasting-color);
          background-color: var(--user-color);
          padding: 2px 8px;
          transition-duration: 0.2s;

          &:hover {
            opacity: 0.8;
          }
        }
      }
    }
  }

  .link-bar {
    display: flex;
    justify-content: space-between;
    gap: 1%;
    margin-top: 10px;
    padding: 0 20px 20px 20px;

    input {
      width: 100%;
      border-radius: 10px;
      background-color: #465586;
      padding: 10px;
      font-size: 16px;

      &:focus {
        outline: none;
      }
    }

    button {
      color: var(--user-contrasting-color);
      background-color: var(--user-color);
      padding: 10px 64px;
      border-radius: 10px;
      font-size: 18px;
      transition-duration: 0.2s;

      &:hover {
        opacity: 0.8;
      }
    }
  }
}
</style>
