// eslint-disable-next-line import/no-named-as-default
import gql from 'graphql-tag'

export const GET_TOKEN_QUERY = gql`
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
`

export const WHOAMI_QUERY = gql`
query {
  whoami {
      username
      email
      isSuperuser
      profileColor
      profilePictureFilename
  }
}
`

export const WHOAMI_NOTES_QUERY = gql`
query {
  whoami {
    notes {
      id
      title
      content
      link
      isPrivate
    }
  }
}
`

export const GET_NOTE_FULL = gql`
query($id: String!) {
  getNote(id: $id) {
      ... on GetNoteSuccess {
          note {
              title
              content
              link
              isPrivate
              creationDate
              tags
              user {
                  username
              }
          }
      }
      ... on RequestValueError {
          details
      }
  }
}
`

export const GET_USER_QUERY = gql`
query($username: String!) {
  getUser(username: $username) {
      __typename
      ... on GetUserSuccess {
          user {
              username
              profilePictureFilename
              isSuperuser

              notes {
                id
                title
                content
                link
                isPrivate
              }
          }
      }
      ... on RequestValueError {
          details
      }
  }
}
`

export const GET_PUBLIC_NOTES = gql`
query ($first: Int, $after: String, $newestFirst: Boolean) {
  getPublicNotes(first: $first, after: $after, newestFirst: $newestFirst) {
      __typename
      ... on NoteConnection {
          pageInfo {
              hasNextPage
              endCursor
          }
          edges {
              node {
                id
                title
                content
                link
                isPrivate
              }
          }
      }
      ... on RequestValueError {
          details
      }
  }
}
`

export const GET_ALL_NOTES = gql`
query ($first: Int, $after: String, $newestFirst: Boolean) {
  getAllNotes(first: $first, after: $after, newestFirst: $newestFirst) {
      __typename
      ... on NoteConnection {
          pageInfo {
              hasNextPage
              endCursor
          }
          edges {
              node {
                id
                title
                content
                link
                isPrivate
              }
          }
      }
      ... on RequestValueError {
          details
      }
  }
}
`
