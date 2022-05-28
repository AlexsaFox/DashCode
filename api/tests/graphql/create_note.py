NOTE_CREATE_QUERY = '''
mutation($title: String!, $content: String!, $tags: [String!], $link: String, $is_private: Boolean) {
    createNote(title: $title, content: $content, tags: $tags, link: $link, isPrivate: $is_private) {
        ... on CreateNoteSuccess {
            note {
                id
                title
                content
                isPrivate
                tags
                user {
                    username
                }
            }
        }
        ... on ValidationError {
            fields {
                field
                details
            }
        }
    }
}
'''
