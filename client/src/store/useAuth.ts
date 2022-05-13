import { defineStore } from 'pinia'
import useErrorsStore from './useErrors'
import apolloClient from '~/modules/apollo'
import config from '~/constants/config'
import { GET_TOKEN_QUERY, WHOAMI_QUERY } from '~/graphql/queries'
import { REGISTER_USER_MUTATION } from '~/graphql/mutations'
import { i18n } from '~/modules/i18n'

export default defineStore('auth', {
  state: () => ({
    loggedIn: localStorage.getItem('loggedIn') ?? false,
    user: (user => user ? JSON.parse(user) : null)(localStorage.getItem('user')),
  }),

  getters: {
    profilePicture(state) {
      const filename = state.user.user.profilePictureFilename
      if (filename !== null)
        return `${config.api_host}/uploads/${filename}`

      else
        return '/src/assets/img/205d9582975737a8b02fb1e5bbc02fd5.jpg'
    },
  },

  actions: {
    async register(username: string, email: string, password: string) {
      const { registerUser } = (await apolloClient.mutate({
        mutation: REGISTER_USER_MUTATION,
        variables: {
          username,
          email,
          password,
        },
      })).data

      if (registerUser.__typename === 'UserAlreadyExists') {
        const { field, value } = registerUser
        useErrorsStore().addError(i18n.global.t('sign-up.errors.user-exists', { field, value }))
      }
      else if (registerUser.__typename === 'ValidationError') {
        const { fields } = registerUser
        for (const { details } of fields)
          useErrorsStore().addError(details)
      }
      else {
        this.login(password, username)
      }
    },

    async login(password: string, username?: string, email?: string) {
      const { token } = (await apolloClient.query({
        query: GET_TOKEN_QUERY,
        variables: {
          username,
          email,
          password,
        },
      })).data

      if (token.__typename === 'RequestValueError') {
        const { details } = token
        useErrorsStore().addError(details)
      }
      else {
        localStorage.setItem('token', token.accessToken)
        await apolloClient.resetStore()
        await this.fetchUser()
      }
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

    async logout() {
      localStorage.removeItem('user')
      localStorage.removeItem('loggedIn')
      this.$reset()
    },
  },
})
