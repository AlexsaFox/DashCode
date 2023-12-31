import { CREATE_NOTE_MUTATION, DELETE_NOTE_MUTATION, EDIT_NOTE_MUTATION } from '~/graphql/mutations'
import { GET_ALL_NOTES, GET_NOTE_FULL, GET_PUBLIC_NOTES, WHOAMI_NOTES_QUERY } from '~/graphql/queries'
import apolloClient from '~/modules/apollo'
import { processCommonErrors } from '~/store/utils'

export async function createNote(title: string, isPrivate: boolean, content: string, tags: string[], link?: string) {
  const { createNote } = (await apolloClient.mutate({
    mutation: CREATE_NOTE_MUTATION,
    variables: {
      title,
      isPrivate,
      content,
      tags,
      link,
    },
  })).data

  if (createNote.__typename !== 'CreateNoteSuccess') {
    processCommonErrors(createNote)
    return null
  }
  return createNote.note.id
}

export async function getNoteFull(id: string) {
  const { getNote } = (await apolloClient.query({
    query: GET_NOTE_FULL,
    variables: {
      id,
    },
  })).data

  if (getNote.__typename !== 'GetNoteSuccess')
    return null

  return getNote.note
}

export async function editNote(id: string, title: string, content: string, tags: string[], link: string, isPrivate: boolean) {
  const { editNote } = (await apolloClient.mutate({
    mutation: EDIT_NOTE_MUTATION,
    variables: {
      noteId: id,
      title,
      content,
      tags,
      link,
      isPrivate,
    },
  })).data

  if (editNote.__typename !== 'EditNoteSuccess')
    processCommonErrors(editNote)
}

export async function deleteNote(id: string) {
  const { removeNote } = (await apolloClient.mutate({
    mutation: DELETE_NOTE_MUTATION,
    variables: {
      id,
    },
  })).data

  if (removeNote.__typename !== 'RemoveNoteSuccess')
    processCommonErrors(removeNote)
}

export async function fetchUserNotes() {
  const { notes } = (await apolloClient.query({
    query: WHOAMI_NOTES_QUERY,
  })).data.whoami
  return notes ?? []
}

export async function getPublicNotes(newestFirst: boolean, first: number, after: string | null) {
  const { getPublicNotes } = (await apolloClient.query({
    query: GET_PUBLIC_NOTES,
    variables: {
      newestFirst,
      first,
      after,
    },
  })).data

  if (getPublicNotes.__typename !== 'NoteConnection') {
    processCommonErrors(getPublicNotes)
    return null
  }
  return getPublicNotes
}

export async function getAllNotes(newestFirst: boolean, first: number, after: string | null) {
  const { getAllNotes } = (await apolloClient.query({
    query: GET_ALL_NOTES,
    variables: {
      newestFirst,
      first,
      after,
    },
  })).data

  if (getAllNotes.__typename !== 'NoteConnection') {
    processCommonErrors(getAllNotes)
    return null
  }
  return getAllNotes
}
