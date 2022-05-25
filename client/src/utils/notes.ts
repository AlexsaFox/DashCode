import { CREATE_NOTE_MUTATION } from '~/graphql/mutations'
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

  if (createNote.__typename !== 'CreateNoteSuccess')
    processCommonErrors(createNote)
}
