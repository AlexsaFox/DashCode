import { GET_USER_QUERY } from '~/graphql/queries'
import apolloClient from '~/modules/apollo'

export async function getUser(username: string) {
  const { getUser } = (await apolloClient.query({
    query: GET_USER_QUERY,
    variables: {
      username,
    },
  })).data

  if (getUser.__typename !== 'GetUserSuccess')
    return null

  return getUser
}
