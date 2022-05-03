// eslint-disable-next-line import/no-named-as-default
import gql from 'graphql-tag'

export const GET_TOKEN_QUERY = gql`
query ($username: String, $email: String, $password: String!) {
  token (username: $username, email: $email, password: $password) {
    accessToken
  }
}
`
export const WHOAMI_QUERY = gql`
query {
  whoami {
    username,
    email,
    profileColor,
    isSuperuser
  }
}
`
