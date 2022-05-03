import { defineStore } from 'pinia'
import apolloClient from '~/modules/apollo'
import { GET_TOKEN_QUERY, WHOAMI_QUERY } from '~/graphql/queries'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    loggedIn: localStorage.getItem('loggedIn') ?? false,
    user: (user => user ? JSON.parse(user) : null)(localStorage.getItem('user')),
  }),

  actions: {
    async login(password: string, username?: string, email?: string) {
      const { token } = (await apolloClient.query({
        query: GET_TOKEN_QUERY,
        variables: {
          username,
          email,
          password,
        },
      })).data

      if (!token)
        return

      localStorage.setItem('token', token.accessToken)
      await apolloClient.resetStore()
      await this.fetchUser()
    },

    async fetchUser() {
      await apolloClient.query({
        query: WHOAMI_QUERY,
      }).then(({ data }) => {
        this.loggedIn = true
        this.user = data.whoami
        localStorage.setItem('loggedIn', JSON.stringify(this.loggedIn))
        localStorage.setItem('user', JSON.stringify(this.user))
      })
    },
  },
})
