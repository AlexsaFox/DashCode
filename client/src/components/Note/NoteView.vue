<script setup lang="ts">
import { deleteNote, getNoteFull } from '~/utils/notes'
import { getTagColor } from '~/utils/colors'
import renderMarkdown from '~/utils/renderMarkdown'
import useAuthStore from '~/store/useAuth'
import useErrorStore from '~/store/useErrors'

const { t } = useI18n()
const router = useRouter()
const auth = useAuthStore()
const errors = useErrorStore()

const { id, editorOpened } = defineProps<{
  id: string
  editorOpened: boolean
}>()

watch(() => editorOpened, () => {
  if (!editorOpened)
    fetchNoteData()
})

const emit = defineEmits<{
  (e: 'loadingFailed'): void
  (e: 'editNote', title: string, content: string, link: string, tags: string[], isPrivate: boolean): void
}>()

const title = ref('')
const content = ref('')
const link = ref('')
const date = ref('')
const tags = ref([] as string[])
const isPrivate = ref(false)
const user = ref({ username: '' })

const markdown = computed(() => {
  return renderMarkdown(content.value)
})
const isOwner = computed(() => {
  return user.value.username === auth.user.username
})

async function fetchNoteData() {
  const note = await getNoteFull(id)

  if (note === null) {
    emit('loadingFailed')
    return
  }

  title.value = note.title
  content.value = note.content
  link.value = note.link
  tags.value = note.tags
  isPrivate.value = note.isPrivate
  user.value = note.user

  const datetimeRegexp = /(\d*)\-(\d*)\-(\d*)T(\d*)\:(\d*)\:(\d*)\.(\d*)/g
  const [, year, monthIdx, day, hour, min, sec, _] = datetimeRegexp.exec(note.creationDate) as RegExpExecArray
  const monthMapping = [
    t('note-show.date.months.january'),
    t('note-show.date.months.february'),
    t('note-show.date.months.march'),
    t('note-show.date.months.april'),
    t('note-show.date.months.may'),
    t('note-show.date.months.june'),
    t('note-show.date.months.july'),
    t('note-show.date.months.august'),
    t('note-show.date.months.september'),
    t('note-show.date.months.october'),
    t('note-show.date.months.november'),
    t('note-show.date.months.december'),
  ]
  const month = monthMapping[parseInt(monthIdx)]
  date.value = `${hour}:${min}:${sec}, ${day} ${month} ${year}`
}

const showDeleteWarning = ref(false)
async function deleteThisNote() {
  await deleteNote(id)
  if (errors.errors.length === 0)
    router.push('/')
}
function editNote() {
  emit('editNote', title.value, content.value, link.value, tags.value, isPrivate.value)
}

onMounted(() => {
  fetchNoteData()
})
</script>

<template>
  <DeleteWarning v-if="showDeleteWarning" @close-popup="showDeleteWarning = false" @delete-note="deleteThisNote" />

  <div class="crutch">
    <section class="main-container">
      <section class="close-bar">
        <button @click="router.push('/')">
          <div class="i-carbon:close" />
        </button>
      </section>

      <section class="title-bar">
        <h2 class="title">
          {{ title }}
        </h2>
        <div class="privacy">
          <p v-if="isPrivate">
            {{ t('note.attributes.privacy.private') }}
          </p>
          <p v-else>
            {{ t('note.attributes.privacy.public') }}
          </p>
        </div>
      </section>

      <section class="content-bar">
        <div class="markdown" readonly v-html="markdown" />
      </section>

      <section v-if="tags.length > 0" class="tag-bar">
        <ul>
          <li v-for="tag in tags" :key="tag" :style="`background-color: ${getTagColor(tag)};`">
            {{ tag }}
          </li>
        </ul>
      </section>

      <section class="link-bar">
        <p v-if="link.length > 0" class="link">
          <a @click="router.push(link)">{{ link }}</a>
        </p>
        <p v-else class="link non-active">
          {{ t('note-show.no-link') }}
        </p>
        <button v-if="isOwner" @click="editNote">
          {{ t('note-show.edit-button') }}
        </button>
        <button v-if="isOwner" @click="showDeleteWarning = true">
          {{ t('note-show.delete-button') }}
        </button>
      </section>

      <section class="user-bar">
        <p>
          {{ t('note-show.created-by') }} <a @click="router.push(`/user/${user.username}`)">{{ user.username }}</a> {{
            t('note-show.created-at')
          }} {{ date }}
        </p>
      </section>
    </section>
  </div>
</template>

<style scoped lang="scss">
@import './note-preview.scss';
</style>
