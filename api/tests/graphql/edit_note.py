NOTE_EDIT_QUERY = '''
mutation($note_id: String! $title: String, $content: String, $tags: [String!], $link: String, $is_private: Boolean, ) {
    editNote(noteId: $note_id, title: $title, content: $content, tags: $tags, link: $link, isPrivate: $is_private) {
        __typename
        ... on EditNoteSuccess {
            note {
                id
                title
                content
                link
                isPrivate
                tags
            }
        }
        ... on ValidationError {
            fields {
                field
                details
            }
        }
        ... on RequestValueError {
            details
        }
    }
}
'''
