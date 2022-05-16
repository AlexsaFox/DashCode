EDIT_ACCOUNT_AUTH_QUERY = '''
mutation($password: String!, $newEmail: String, $newPassword: String) {
    editAccountAuth(password: $password, newEmail: $newEmail, newPassword: $newPassword) {
        __typename
        ... on EditAccountSuccess {
            account {
                email
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
        ... on UserAlreadyExists {
            field
            value
        }
    }
}
'''
