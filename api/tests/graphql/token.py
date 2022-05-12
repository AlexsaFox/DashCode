TOKEN_QUERY = '''
query($username: String, $email: String, $password: String!) {
    token(username: $username, email: $email, password: $password) {
        __typename
        ... on RequestValueError {
            details
        }
        ... on Token {
            accessToken
            tokenType
        }
    }
}
'''
