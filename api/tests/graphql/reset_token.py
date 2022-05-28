RESET_TOKEN_QUERY = '''
mutation($password: String!) {
    resetToken(password: $password) {
        __typename
        ... on RequestValueError {
            details
        }
        ... on ResetTokenSuccess {
            token {
                accessToken
                tokenType
            }
        }
    }
}
'''
