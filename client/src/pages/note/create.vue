<script setup lang="ts">
import { useVuelidate } from '@vuelidate/core'
import useErrors from '~/store/useErrors'
import checkFormErrors from '~/utils/checkFormErrors'
import { createNote } from '~/utils/notes'

const rules = reactive({
  title: {},
  isPrivate: {},
  content: {},
  tags: {},
  link: {},
})

function saveNote(title: string, isPrivate: boolean, content: string, tags: string[], link?: string) {
  const vuelidate = useVuelidate(rules, { title, isPrivate, content, tags, link })
  checkFormErrors(
    vuelidate,
    async() => { return (await createNote(title, isPrivate, content, tags, link)) },
    () => { useErrors().addError('Successfully saved note! (Temporary message, will be replaced by redirect to page with created note in the future)') },
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
