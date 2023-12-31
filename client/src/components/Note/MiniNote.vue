<script setup lang="ts">
import renderMarkdown from '~/utils/renderMarkdown'

const { t } = useI18n()
const router = useRouter()

const { note } = defineProps<{
  note: {
    id: string
    title: string
    isPrivate: boolean
    content: string
    link: string
  }
}>()

function getDomain(link: string) {
  if (link === '')
    return t('note-show.no-link')

  const domainRegexp = /\:\/\/(.*?)(\/|$)/g
  const matches = domainRegexp.exec(link)
  if (matches === null || matches.length < 2)
    // Fallback, this shouldn't happen
    return link

  return matches[1]
}
</script>

<template>
  <div class="note-base" @click="router.push(`/note/${note.id}`)">
    <h3>{{ note.title }}</h3>
    <div class="privacy">
      <div v-if="note.isPrivate" class="i-carbon:locked" />
      <div v-else class="i-carbon:unlocked" />
    </div>
    <div class="note-content">
      <p v-html="renderMarkdown(note.content)" />
      <div class="note-link">
        <p :class="(note.link === '' ? ' non-active' : '')">
          {{ getDomain(note.link) }}
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped  lang="scss">
@import '/src/assets/scss/markdown-config.scss';

.note-base {
  $note-size: 300px;
  $note-padding: 10px;

  position: relative;
  background-color: #223153;
  padding: $note-padding;
  margin: 15px;
  border-radius: 10px;
  height: $note-size;
  width: $note-size;

  h3 {
    width: 85%;
    font-size: 22px;
    padding-left: 3px;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .privacy {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 22px;
  }

  transition-duration: 0.5s;

  &:hover {
    cursor: pointer;
    transform: translateY(-8px);
    transition-duration: 0.2s;
  }

  .note-content {
    position: absolute;
    bottom: $note-padding;
    left: $note-padding;
    width: $note-size - 2*$note-padding;
    height: 240px;
    background-color: #5B6B98;
    border-radius: 10px;
    padding: 10px;
    overflow: hidden;

    &::v-deep(p) {
      @include markdown-config;

      &::v-deep(pre) {
        overflow-x: hidden;
        text-overflow: ellipsis;
        padding: 8px 8px;
      }

      font-size: 16px;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .note-link {
      position: absolute;
      bottom: 0;
      left: 0;
      width: 100%;
      padding: 10px;
      background-color: #465586;
      border-top: 10px solid #5B6B98;

      &>p {
        font-size: 16px;
        text-align: center;
        overflow: hidden;
        text-overflow: ellipsis;

        &.non-active {
          opacity: 0.3;
        }
      }
    }
  }
}
</style>
