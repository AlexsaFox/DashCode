DELETE_USER_QUERY = '''
mutation($password: String!) {
    deleteUser(password: $password) {
        __typename
        ... on RequestValueError {
            details
        }
        ... on DeleteUserSuccess {
            account {
                username
            }
        }
    }
}
'''
