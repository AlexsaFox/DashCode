GET_PUBLIC_NOTES_QUERY = '''
query ($first: Int, $after: String, $newestFirst: Boolean) {
    getPublicNotes(first: $first, after: $after, newestFirst: $newestFirst) {
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
