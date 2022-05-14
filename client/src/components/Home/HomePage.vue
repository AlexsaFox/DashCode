<template>
  <div class="space_for_notes">
    <div class="main_body_for_note">
      <button>
        <a class="button_for_pop_up" href="{{url_for('webapp.note.notes_show_handler', note_id=id)}}">
          <div class="title_for_main_note"><span>note.title</span></div>
          <div class="public_private">
            <span>
              <div class="i-carbon:unlocked" />
            </span>
          </div>
          <div class="delete"><span>
            <div class="i-carbon:trash-can" />
          </span></div>
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
          <div class="title_for_main_note"><span>note.title</span></div>
          <div class="public_private">
            <span>
              <div class="i-carbon:unlocked" />
            </span>
          </div>
          <div class="delete"><span>
            <div class="i-carbon:trash-can" />
          </span></div>
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
          <div class="title_for_main_note"><span>note.title</span></div>
          <div class="public_private">
            <span>
              <div class="i-carbon:unlocked" />
            </span>
          </div>
          <div class="delete"><span>
            <div class="i-carbon:trash-can" />
          </span></div>
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
  <NavButtons />
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

  .header_for_public {
    color: white;
    font-size: 120%;
    font-family: 'ClearSans-Regular';
  }

  .main_body_for_note {
    display: inline-block;
    background-color: #223153;
    width: 200px;
    height: 233px;
    margin-right: 1.5%;
    margin-left: 1.5%;
    margin-bottom: 3%;
    border-radius: 15px;
    font-size: 120%;
    padding: 0px 0.5%;
    transition: 0.5s;

  }

  .main_body_for_note span {
    font-family: 'ClearSans-Regular';
    color: white;
    text-decoration: none;
    font-size: 85%;
    border: none;
    width: inherit;
    height: inherit;

  }

  .main_body_for_note:hover {
    transition: 0.5s;
    width: 205px;
    height: 236px;
    font-size: 123%;
    margin-right: 1.25%;
    margin-left: 1.25%;
    margin-bottom: 2%;
  }

  .title_for_main_note {
    overflow: hidden;
    text-overflow: ellipsis;
    height: 25px;
  }

  .title {
    display: inline-block;
  }

  .notes_author {
    margin-left: 25%;
    font-size: 80%;
    display: inline-block;
  }

  .notes_author span {
    color: var(--primary-color);
  }

  .note {
    font-family: 'ClearSans-Light';
    background-color: #5B6B98;
    border-radius: 8px 8px 0px 0px;
    padding: 2%;
    height: 140px;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .note span {
    font-family: 'ClearSans-Light';
    color: white;
    font-size: 80%;
    padding: 3%;
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
  }

  .link span {
    font-size: 70%;
    padding: 3%;
    font-family: 'ClearSans-Light';
    color: white;
    text-align: center;
  }

  .public_private {
    display: inline-block;

    div {
      color: white;
    }
  }

  .delete {
    margin-left: 5px;
    display: inline-block;

    div {
      color: white;
    }
  }
}
</style>
