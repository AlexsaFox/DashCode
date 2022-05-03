import { defineStore } from 'pinia'

export default defineStore('errors', {
  state: () => ({
    errors: [] as Array<string>,
  }),

  actions: {
    removeError(error: string) {
      this.errors = this.errors.filter(err => err !== error)
    },

    addError(error: string) {
      // If error already exists, it will disappear,
      // then appear again on the next frame. End user
      // will not be able to notice that delay. However,
      // that will be enough for Vue to notice that list
      // have been changed, so v-for in <ErrorIndicator />
      // will render again, so fade-in animation will be triggered,
      // which should result in user noticing that error was
      // caused again
      this.removeError(error)
      nextTick(() => { this.errors.push(error) })
    },
  },
})
