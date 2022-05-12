REGISTRATION_QUERY = '''
mutation ($username: String!, $email: String!, $password: String!) {
    registerUser(username: $username, email: $email, password: $password) {
        __typename
        ... on UserAlreadyExists {
            field
            value
        }
        ... on RegisterUserSuccess {
            account {
                user {
                    username
                    profileColor
                    isSuperuser
                    profilePictureFilename
                }
                email
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
