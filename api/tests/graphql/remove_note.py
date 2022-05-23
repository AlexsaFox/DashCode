NOTE_REMOVE_QUERY = '''
mutation($id: String!){
    removeNote(id: $id){
        __typename
        ... on RemoveNoteSuccess {
            note {
                id
                title
                content
                link
                isPrivate
            }
        }
        ... on RequestValueError{
            details
        }
    }
}
'''
