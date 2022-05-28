<script setup lang="ts">
const { t } = useI18n()
const router = useRouter()
</script>

<template>
  <div class="space_for_notes">
    <div class="main_body_for_note">
      <button>
        <a class="button_for_pop_up" href="{{url_for('webapp.note.notes_show_handler', note_id=id)}}">
          <div class="block_for_header">
            <div class="title_for_main_note"><span>note.title</span></div>
            <div class="public_private">
              <span>
                <div class="i-carbon:unlocked" />
              </span>
            </div>
          </div>
          <!-- <div class="public_private"><span><i class='bx bx-lock-open-alt'></i></span></div> -->
          <div class="note">
            <span>note.context</span>
          </div>
          <div class="link">
            <span>note.link</span>
          </div>
        </a>
      </button>
    </div>
    <div class="main_body_for_note">
      <button>
        <a class="button_for_pop_up" href="{{url_for('webapp.note.notes_show_handler', note_id=id)}}">
          <div class="block_for_header">
            <div class="title_for_main_note"><span>note.title</span></div>
            <div class="public_private">
              <span>
                <div class="i-carbon:unlocked" />
              </span>
            </div>
          </div>
          <!-- <div class="public_private"><span><i class='bx bx-lock-open-alt'></i></span></div> -->
          <div class="note">
            <span>note.context</span>
          </div>
          <div class="link">
            <span>note.link</span>
          </div>
        </a>
      </button>
    </div>
    <div class="main_body_for_note">
      <button>
        <a class="button_for_pop_up" href="{{url_for('webapp.note.notes_show_handler', note_id=id)}}">
          <div class="block_for_header">
            <div class="title_for_main_note"><span>note.title</span></div>
            <div class="public_private">
              <span>
                <div class="i-carbon:unlocked" />
              </span>
            </div>
          </div>
          <!-- <div class="public_private"><span><i class='bx bx-lock-open-alt'></i></span></div> -->
          <div class="note">
            <span>note.context</span>
          </div>
          <div class="link">
            <span>note.link</span>
          </div>
        </a>
      </button>
    </div>
    <div class="main_body_for_note">
      <button>
        <a class="button_for_pop_up" href="{{url_for('webapp.note.notes_show_handler', note_id=id)}}">
          <div class="block_for_header">
            <div class="title_for_main_note"><span>note.title</span></div>
            <div class="public_private">
              <span>
                <div class="i-carbon:unlocked" />
              </span>
            </div>
          </div>
          <!-- <div class="public_private"><span><i class='bx bx-lock-open-alt'></i></span></div> -->
          <div class="note">
            <span>note.context</span>
          </div>
          <div class="link">
            <span>note.link</span>
          </div>
        </a>
      </button>
    </div>
  </div>
  <NavigationPanel>
    <NavigationButton
      @on-press="router.push('/note/create')"
    >
      <div class="i-carbon:add" /> {{ t('index.home.side-buttons.add-notes') }}
    </NavigationButton>
    <NavigationButton
      @on-press="router.push('/')"
    >
      <div class="i-carbon:arrow-right" /> {{ t('index.home.side-buttons.explore') }}
    </NavigationButton>
  </NavigationPanel>
</template>

<style scoped lang="scss">
.space_for_notes {
  display: inline-block;
  width: 70%;
  margin-top: 70px;
  margin-left: 10%;

  button {
    border: none;
    text-decoration: none;
    width: 100%;
    text-align: left;
    font-size: 100%;
  }

  .main_body_for_note {
    display: inline-block;
    background-color: #223153;
    width: 200px;
    height: 223px;
    margin-right: 1.5%;
    margin-left: 1.5%;
    margin-bottom: 3%;
    border-radius: 15px;
    font-size: 120%;
    padding: 0px 0.5%;
    transition: 0.6s;
    &:hover{
       transform: translateY(-10px);
    }
    .block_for_header{
      display: flex;
      justify-content: space-between;
      margin: 5px;
    }
    span{
      font-family: 'ClearSans-Regular';
      color: white;
      text-decoration: none;
      font-size: 85%;
      border: none;
      width: inherit;
      height: inherit;
    }
  }

  .title_for_main_note {
    overflow: hidden;
    text-overflow: ellipsis;
    height: 28px;
    display: inline-block;
  }

  .note {
    font-family: 'ClearSans-Light';
    background-color: #5B6B98;
    border-radius: 8px 8px 0px 0px;
    padding: 2%;
    height: 140px;
    overflow: hidden;
    text-overflow: ellipsis;
    span{
      font-family: 'ClearSans-Light';
      color: white;
      font-size: 80%;
      padding: 3%;
    }
  }

  .link {
    height: 35px;
    font-family: 'ClearSans-Light';
    background-color: #465586;
    border-radius: 0px 0px 8px 8px;
    padding: 2%;
    text-align: center;
    overflow: hidden;
    text-overflow: ellipsis;
    span{
      font-size: 70%;
      padding: 3%;
      font-family: 'ClearSans-Light';
      color: white;
      text-align: center;
    }
  }

  .public_private {
    margin-top: 5px;
    div {
      color: white;
    }
  }
}
</style>
