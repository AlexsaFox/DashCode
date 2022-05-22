GET_PUBLIC_NOTES_QUERY = '''
query ($first: Int, $after: String) {
    getPublicNotes(first: $first, after: $after) {
        __typename
        ... on NoteConnection {
            pageInfo {
                hasNextPage
                startCursor
                endCursor
            }
            edges {
                node {
                    id
                    title
                    isPrivate
                    user {
                        username
                    }
                }
                cursor
            }
        }
        ... on RequestValueError {
            details
        }
    }
}
'''
