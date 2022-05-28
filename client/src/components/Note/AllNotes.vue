<script setup lang="ts">
import { getAllNotes } from '~/utils/notes'

const { t } = useI18n()

const NOTES_PER_LOAD = 20

const loadedNotes = ref([] as any[])
let loadInProcess = false
let hasNextPage = true
let cursor = null as null | string

const sortSelectorValue = ref('new')
const newerFirst = computed(() => {
  return sortSelectorValue.value === 'new'
})
watch(sortSelectorValue, () => { refresh() })

function refresh() {
  loadedNotes.value = []
  hasNextPage = true
  cursor = null
  loadNotes()
}

async function loadNotes() {
  if (hasNextPage && !loadInProcess) {
    loadInProcess = true
    const connection = await getAllNotes(newerFirst.value, NOTES_PER_LOAD, cursor)
    for (let i = 0; i < connection.edges.length; i++) {
      const newNote = connection.edges[i].node
      loadedNotes.value.push(newNote)
    }
    cursor = connection.pageInfo.endCursor
    hasNextPage = connection.pageInfo.hasNextPage

    loadInProcess = false
  }
}

const LOAD_WHEN_X_LINES_BEFORE_END = 2
const NOTE_HEIGHT = 330
window.onscroll = () => {
  const topBorder = document.documentElement.scrollTop
  const windowHeight = window.innerHeight
  const docHeight = document.documentElement.scrollHeight

  if (topBorder + windowHeight + LOAD_WHEN_X_LINES_BEFORE_END * NOTE_HEIGHT >= docHeight)
    loadNotes()
}

await loadNotes()
</script>

<template>
  <header>
    <div class="container">
      <h3>
        {{ t('administrate.header.header') }}
      </h3>
      <div class="sort-selector">
        <p>{{ t('explore.header.sort-by') }}</p>
        <select v-model="sortSelectorValue">
          <option value="new">
            {{ t('explore.header.from-newest') }}
          </option>
          <option value="old">
            {{ t('explore.header.from-oldest') }}
          </option>
        </select>
      </div>
    </div>
  </header>

  <hr class="separator">

  <section class="user-notes">
    <MiniNote v-for="note in loadedNotes" :key="note" :note="note" />
  </section>
</template>

<style scoped lang="scss">
header {
  width: 70%;
  margin-top: 70px;
  margin-left: 5%;

  h3 {
    color: white;
    font-family: 'ClearSans-Bold';
    font-size: 36px;
    padding: 5px;
  }

  .container {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;

    .sort-selector {
      display: flex;
      align-items: flex-end;
      font-family: 'ClearSans-Regular';
      font-size: 20px;
      margin: 12px 0;

      p {
        padding: 4px 0;
      }

      select {
        margin: 0 10px;
        background-color: #303D67;
        border-radius: 10px;
        padding: 5px;

        &:focus {
          outline: none;
        }
      }
    }
  }
}

.separator {
  border: #5B6B98 solid 2px;
  width: 70%;
  margin-left: 5%;
  border-radius: 5px;
}

.user-notes {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  width: 70vw;
  margin-left: 5%;
  margin-top: 70px;
  user-select: none;
}
</style>
