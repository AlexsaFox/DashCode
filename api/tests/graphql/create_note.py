NOTE_CREATE_QUERY = '''
mutation($title: String!, $content: String!, $link: String, $is_private: Boolean, ) {
    createNote(title: $title, content: $content, link: $link, isPrivate: $is_private) {
        ... on Note {
            id
            title
            content
            isPrivate

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
