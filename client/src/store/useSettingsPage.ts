import { defineStore } from 'pinia'
import Pages from '~/constants/types/pages'

export default defineStore('settingsPage', {
  state: () => ({
    currentPage: Pages.MyAccountPage,
  }),

  actions: {
    changePage(page: Pages) {
      this.currentPage = page
    },
  },
})
