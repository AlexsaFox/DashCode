EDIT_ACCOUNT_QUERY = '''
mutation($newUsername: String, $newProfileColor: String) {
    editAccount(newUsername: $newUsername, newProfileColor: $newProfileColor) {
        __typename
        ... on EditAccountSuccess {
            account {
                username
                profileColor
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
