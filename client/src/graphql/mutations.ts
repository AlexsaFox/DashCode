// eslint-disable-next-line import/no-named-as-default
import gql from 'graphql-tag'

export const REGISTER_USER_MUTATION = gql`
mutation($username: String!, $email: String!, $password: String!) {
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

`

export const EDIT_USER_AUTH_MUTATION = gql`
mutation($password: String!, $newPassword: String, $newEmail: String) {
  editAccountAuth(password: $password, newPassword: $newPassword, newEmail: $newEmail) {
      __typename
      ... on EditAccountSuccess {
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
      ... on RequestValueError {
          details
      }
  }
}
`
