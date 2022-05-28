<script setup lang="ts">
import { useVuelidate } from '@vuelidate/core'
import { helpers, maxLength, required, url } from '@vuelidate/validators'
import useErrorStore from '~/store/useErrors'
import checkFormErrors from '~/utils/checkFormErrors'
import { createNote } from '~/utils/notes'

const { t } = useI18n()
const errors = useErrorStore()
const router = useRouter()

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

function saveNote(title: string, isPrivate: boolean, content: string, tags: string[], link?: string) {
  const vuelidate = useVuelidate(rules, { title, isPrivate, content, tags, link })
  checkFormErrors(
    vuelidate,
    async() => {
      await createNote(title, isPrivate, content, tags, link).then((id) => {
        if (errors.errors.length === 0 && id !== null)
          router.push(`/note/${id}`)
      })
    },
  )
}
</script>

<template>
  <edit-note :save-action="saveNote" />
  <NavButtons />
</template>

<route lang="yaml">
meta:
  requiresAuth: true
</route>
