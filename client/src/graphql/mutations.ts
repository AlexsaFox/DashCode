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
            username
            profileColor
            isSuperuser
            profilePictureFilename
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
              username
              profileColor
              isSuperuser
              profilePictureFilename
              email
          }
      }
      ... on UserAlreadyExists {
          field
          value
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

export const EDIT_USER_MUTATION = gql`
mutation($newUsername: String, $newProfileColor: String, $newProfilePicture: Upload) {
  editAccount(newUsername: $newUsername, newProfileColor: $newProfileColor, newProfilePicture: $newProfilePicture) {
      __typename
      ... on EditAccountSuccess {
          account {
              username
              profileColor
              profilePictureFilename
          }
      }
      ... on UserAlreadyExists {
          field
          value
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

export const DELETE_USER_MUTATION = gql`
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
}`

export const CREATE_NOTE_MUTATION = gql`
mutation($title: String!, $content: String!, $tags: [String!], $link: String, $isPrivate: Boolean) {
  createNote(title: $title, content: $content, tags: $tags, link: $link, isPrivate: $isPrivate) {
      ... on CreateNoteSuccess {
          note {
              id
              title
              content
              isPrivate
              tags
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
