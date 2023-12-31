NOTE_GET_QUERY = '''
query($id: String!) {
    getNote(id: $id) {
        ... on GetNoteSuccess {
            note {
                id
                title
                content
                link
                isPrivate
                tags
            }
        }
        ... on RequestValueError {
            details
        }
    }
}
'''
