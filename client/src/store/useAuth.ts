import { defineStore } from 'pinia'
import useErrorsStore from './useErrors'
import { nullIfEmpty, processCommonErrors } from './utils'
import apolloClient from '~/modules/apollo'
import config from '~/constants/config'
import { GET_TOKEN_QUERY, WHOAMI_QUERY } from '~/graphql/queries'
import { EDIT_USER_AUTH_MUTATION, EDIT_USER_MUTATION, REGISTER_USER_MUTATION } from '~/graphql/mutations'
import { i18n } from '~/modules/i18n'

const useAuthStore = defineStore('auth', {
  state: () => ({
    loggedIn: localStorage.getItem('loggedIn') ?? false,
    user: (user => user ? JSON.parse(user) : null)(localStorage.getItem('user')),
  }),

  getters: {
    profilePicture(state) {
      const filename = state.user.profilePictureFilename
      return filename === null ? null : `${config.api_host}/uploads/${filename}`
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

      const errors = useErrorsStore()
      if (registerUser.__typename === 'UserAlreadyExists') {
        const { field, value } = registerUser
        errors.addError(i18n.global.t('sign-up.errors.user-exists', { field, value }))
      }
      else if (registerUser.__typename !== 'RegisterUserSuccess') {
        processCommonErrors(registerUser)
      }
      else {
        await this.login(password, username)
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

      if (token.__typename !== 'Token') {
        processCommonErrors(token)
      }
      else {
        localStorage.setItem('token', token.accessToken)
        await apolloClient.resetStore()
        await this.fetchUser()
      }
    },

    async editAuth(currentPassword: string, email?: string, password?: string) {
      const { editAccountAuth } = (await apolloClient.mutate({
        mutation: EDIT_USER_AUTH_MUTATION,
        variables: {
          newEmail: email,
          newPassword: nullIfEmpty(password),
          password: currentPassword,
        },
      })).data

      if (editAccountAuth.__typename === 'UserAlreadyExists') {
        const { field, value } = editAccountAuth
        useErrorsStore().addError(i18n.global.t('sign-up.errors.user-exists', { field, value }))
      }
      else if (editAccountAuth.__typename !== 'EditAccountSuccess') { processCommonErrors(editAccountAuth) }
      else { await this.fetchUser() }
    },

    async edit(profileColor?: string, username?: string) {
      const { editAccount } = (await apolloClient.mutate({
        mutation: EDIT_USER_MUTATION,
        variables: {
          newProfileColor: nullIfEmpty(profileColor),
          newUsername: nullIfEmpty(username),
        },
      })).data

      if (editAccount.__typename === 'UserAlreadyExists') {
        const { field, value } = editAccount
        useErrorsStore().addError(i18n.global.t('sign-up.errors.user-exists', { field, value }))
      }
      else if (editAccount.__typename !== 'EditAccountSuccess') { processCommonErrors(editAccount) }
      else { await this.fetchUser() }
    },

    async editProfilePicture(file: File) {
      const { editAccount } = (await apolloClient.mutate({
        mutation: EDIT_USER_MUTATION,
        variables: {
          newProfilePicture: file,
        },
        context: {
          hasUpload: true,
        },
      })).data

      if (editAccount.__typename !== 'EditAccountSuccess')
        processCommonErrors(editAccount)

      else
        await this.fetchUser()
    },

    async fetchUser() {
      const { data } = await apolloClient.query({
        query: WHOAMI_QUERY,
      })

      this.$state = {
        loggedIn: true,
        user: data.whoami,
      }
      localStorage.setItem('loggedIn', JSON.stringify(this.loggedIn))
      localStorage.setItem('user', JSON.stringify(this.user))
    },

    async logout() {
      localStorage.removeItem('user')
      localStorage.removeItem('loggedIn')
    },
  },
})

export default useAuthStore
