<script setup lang="ts">
import { fetchUserNotes } from '~/utils/notes'

const { t } = useI18n()
const router = useRouter()

const notes = await fetchUserNotes()

</script>

<template>
  <div class="crunch">
    <section class="note-container">
      <MiniNote v-for="note in notes" :key="note" :note="note" />
    </section>
  </div>

  <NavigationPanel>
    <NavigationButton @on-press="router.push('/note/create')">
      <div class="i-carbon:add" /> {{ t('index.home.side-buttons.add-notes') }}
    </NavigationButton>
    <NavigationButton @on-press="router.push('/')">
      <div class="i-carbon:arrow-right" /> {{ t('index.home.side-buttons.explore') }}
    </NavigationButton>
  </NavigationPanel>
</template>

<style scoped lang="scss">
@import '/src/assets/scss/markdown-config.scss';

.crunch {
  border: 0.1px solid transparent;
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
