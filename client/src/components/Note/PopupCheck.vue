<script setup lang="ts">
import noteEditActions from '~/constants/types/noteEditActions'
const { t } = useI18n()

const emit = defineEmits<{
  (e: 'action', action: noteEditActions): void
}>()

function cancel() { emit('action', noteEditActions.cancel) }
function discard() { emit('action', noteEditActions.discard) }
function save() { emit('action', noteEditActions.save) }
</script>

<template>
  <div class="overlay">
    <div class="popup_check">
      <div class="header_for_pop_up">
        <a class="close" @click="cancel">&times;</a>
      </div>
      <div class="content">
        <span>{{ t("note-edit.warning-label") }}</span>
        <div class="buttons_for_check">
          <div class="each_button_for_popup_check">
            <button @click="save">
              {{ t('note-edit.save-button') }}
            </button>
          </div>
          <div class="each_button_for_popup_check">
            <button @click="discard">
              {{ t('note-edit.unsave-button') }}
            </button>
          </div>
          <div class="each_button_for_popup_check">
            <button @click="cancel">
              {{ t('note-edit.cancel-button') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped lang="scss">
.overlay {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7);
  transition: opacity 500ms;
  height: 100%;
  z-index: 10;
  overflow-y: auto;
}

.popup_check {
  margin: 70px auto;
  background: #5B6B98;
  border-radius: 10px;
  width: 80%;
  max-width: 700px;
  position: relative;
  padding-top: 20px;
}

.popup_check .close {
  position: absolute;
  top: 10px;
  right: 20px;
  transition: all 200ms;
  font-size: 240%;
  font-weight: bold;
  text-decoration: none;
  color: #F1F7ED;
}

.popup_check .content {
  font-family: 'ClearSans-Light';
  text-align: center;
  color: white;
  font-size: 120%;

}

.popup_check .buttons_for_check {
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: center;
  gap: 10px;

  button {
    font-size: 16px;
    font-family: 'ClearSans-Regular';
    background-color: #86faf8;
    color: #223153;
    border-radius: 5px;
    border: none;
    padding: 10px 32px;
    cursor: pointer;

    &:hover {
      opacity: 0.8;
    }
  }
}

.popup_check .buttons_for_check {
  margin: 5% 0px;
  padding-bottom: 2%;
}

.each_button_for_popup_check {
  display: inline-block;
}
</style>
