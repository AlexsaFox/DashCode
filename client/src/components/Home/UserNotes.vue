<script setup lang="ts">
import { fetchUserNotes } from '~/utils/notes'
const notes = await fetchUserNotes()
</script>

<template>
  <div class="crunch">
    <section class="note-container">
      <MiniNote v-for="note in notes" :key="note" :note="note" />
    </section>
  </div>
</template>

<style scoped lang="scss">
@import '/src/assets/scss/markdown-config.scss';

.crunch {
  border: 1px solid transparent;
}

.note-container {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  width: 70%;
  margin-left: 5%;
  margin-top: 70px;
  user-select: none;
}
</style>
