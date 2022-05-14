import {
  ApolloClient,
  InMemoryCache,
  createHttpLink,
} from '@apollo/client/core'
import { setContext } from '@apollo/client/link/context'
import { onError } from '@apollo/client/link/error'
import config from '~/constants/config'
import useErrorsStore from '~/store/useErrors'

const httpLink = createHttpLink({
  uri: config.graphql_host,
})

const graphQLErrorLink = onError(({ graphQLErrors }) => {
  if (graphQLErrors) {
    const errors = useErrorsStore()
    for (const error of graphQLErrors)
      errors.addError(error.message)
  }
})

const authLink = setContext((_, { headers }) => {
  const token = localStorage.getItem('token')
  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : '',
    },
  }
})

const apolloClient = new ApolloClient({
  link: authLink.concat(graphQLErrorLink.concat(httpLink)),
  cache: new InMemoryCache(),
})

export default apolloClient
