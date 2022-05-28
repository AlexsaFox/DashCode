<script setup lang="ts">
import { useVuelidate } from '@vuelidate/core'
import { helpers, maxLength, required, url } from '@vuelidate/validators'
import checkFormErrors from '~/utils/checkFormErrors'
import { editNote } from '~/utils/notes'

const { t } = useI18n()
const router = useRouter()

const { id } = defineProps<{
  id: string
}>()

const noteEditorOpened = ref(false)
const note = reactive({
  title: '',
  content: '',
  link: '',
  tags: [] as string[],
  isPrivate: true,
})
function openNoteEditor(title: string, content: string, link: string, tags: string[], isPrivate: boolean) {
  noteEditorOpened.value = !noteEditorOpened.value
  note.title = title
  note.content = content
  note.link = link
  note.tags = tags
  note.isPrivate = isPrivate
}

const rules = reactive({
  title: {
    required: helpers.withMessage(t('note-edit.errors.title.required'), required),
    maxlength: helpers.withMessage(t('note-edit.errors.title.maxlength'), maxLength(65)),
  },
  content: {
    required: helpers.withMessage(t('note-edit.errors.content.required'), required),
  },
  link: {
    url: helpers.withMessage(t('note-edit.errors.link.url'), url),
  },
  tags: {
    tagLength: helpers.withMessage(
      t('note-edit.errors.tags.tag-length'),
      (tags: string[]) => { return tags.every((tag) => { return tag.length <= 30 }) },
    ),
    tagCharset: helpers.withMessage(
      t('note-edit.errors.tags.tag-charset'),
      (tags: string[]) => {
        return tags.every((tag) => {
          for (let i = 0; i < tag.length; i++) {
            const letterCode = tag.charCodeAt(i)
            if (!( // If not among following symbols:
              (letterCode >= 97 && letterCode <= 122) // a-z
                || (letterCode >= 48 && letterCode <= 57) // 0-9
                || (letterCode === 45) // - (dash symbol)
            ))
              return false
          }
          return true
        })
      },
    ),
  },
  isPrivate: {
    required: helpers.withMessage(t('note-edit.errors.privacy.required'), required),
  },
})

function loadingFailed() {
  router.push('/not-found')
}

function saveEdited(title: string, isPrivate: boolean, content: string, tags: string[], link?: string) {
  const vuelidate = useVuelidate(rules, { title, isPrivate, content, tags, link })
  checkFormErrors(
    vuelidate,
    async() => { await editNote(id, title, content, tags, link ?? '', isPrivate) },
    () => { noteEditorOpened.value = false },
  )
}
</script>

<template>
  <EditNote
    v-if="noteEditorOpened"
    :title="note.title"
    :content="note.content"
    :link="note.link"
    :tags="note.tags"
    :is-private="note.isPrivate"
    :save-action="saveEdited"
  />
  <Suspense v-else>
    <template #default>
      <NoteView :id="id" :editor-opened="noteEditorOpened" @loading-failed="loadingFailed" @edit-note="openNoteEditor" />
    </template>
    <template #fallback>
      <h1>Loading</h1>
    </template>
  </Suspense>

  <NavigationPanel>
    <NavigationButton
      @on-press="router.push('/note/create')"
    >
      <div class="i-carbon:add" /> {{ t('index.home.side-buttons.add-notes') }}
    </NavigationButton>
    <NavigationButton
      @on-press="router.push('/')"
    >
      <div class="i-carbon:arrow-right" /> {{ t('index.home.side-buttons.explore') }}
    </NavigationButton>
    <NavigationButton
      @on-press="router.push('/')"
    >
      <div class="i-carbon:home" /> {{ t('index.home.side-buttons.go-home') }}
    </NavigationButton>
  </NavigationPanel>
</template>

<route lang="yaml">
meta:
  requiresAuth: true
</route>
