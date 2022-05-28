USER_GET_QUERY = '''
query($username: String!) {
    getUser(username: $username) {
        __typename
        ... on GetUserSuccess {
            user {
                username
            }
        }
        ... on RequestValueError {
            details
        }
    }
}
'''
