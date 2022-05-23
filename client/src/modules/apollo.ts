import {
  ApolloClient,
  InMemoryCache,
} from '@apollo/client/core'
import { createUploadLink } from 'apollo-upload-client'
import { setContext } from '@apollo/client/link/context'
import { onError } from '@apollo/client/link/error'
import config from '~/constants/config'
import useErrorsStore from '~/store/useErrors'

const uploadLink = createUploadLink({
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
  link: authLink.concat(graphQLErrorLink.concat(uploadLink)),
  cache: new InMemoryCache(),
  defaultOptions: {
    query: {
      fetchPolicy: 'no-cache',
    },
    watchQuery: {
      fetchPolicy: 'no-cache',
    },
  },
})

export default apolloClient
