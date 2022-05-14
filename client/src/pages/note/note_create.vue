<script setup lang="ts">
const { t } = useI18n()

</script>
<template>
  <div class="overlay_for_space_for_note_edit_and_show">
    <div class="space_for_note_edit_and_show">
      <!-- {% with id = request.environ['note_id'] %} -->

      <!-- {% endwith %}

        {{ form.csrf_token }} -->
      <input placeholder="title" class="input_for_title">
      <select class="privacy_selection">
        <option value="private">
          private
        </option>
        <option value="public">
          public
        </option>
      </select>
      <a href="#popup_check"><button onclick="location.href='{{ url_for('webapp.index.index_view') }}'" class="button_back_to_all_notes">
        <div class="i-carbon:close" />
      </button></a>
      <PopupCheck />
      <div class="content">
        <textarea class="comment" placeholder="text" cols="80" rows="11" />
        <textarea class="textarea_for_link" placeholder="https://" cols="90" rows="1" />

        <!-- {% with id=request.environ['note_id'] %} -->
        <input type="submit" class="save" :value="t('note_create.create-button')">

        <!-- {% endwith %} -->
      </div>
    </div>
  </div>
  <NavButtons />
  <!-- {% endwith %} -->
</template>
<style>
.space_for_note_edit_and_show .input_for_title{
    font-family: 'ClearSans-Light';
    color:white;
    background-color: rgba(255, 255, 255, 0.1);
    text-align:left;
    padding: 10px;
    border-radius: 10px;
    font-size: 20px;
    margin: 0px 0px 20px 20px;
    color: #F1F7ED;
    width: 80%;
    border:none;
    resize: none;

}
.privacy_selection{
    font-family: 'ClearSans-Light';
    background-color: rgba(43, 59, 95, 0.75);
    color: white;
    border-radius: 10px;
    font-size: 80%;
    border: none;
    width: 8%;
    padding: 2px 0px;
    text-align: center;
    margin-left: 1% ;
}
.save{
    background-color: #86faf8;
    border-radius: 8px;
    font-size: 120%;
    color:white;
    font-family: 'ClearSans-Bold';
    color:#223153;
    text-decoration: none;
    text-align: center;
    vertical-align:top;
    padding: 9px 5%;
    cursor: pointer;
    border: none;
    width: 15%;
    margin-top: 20px;
    display: inline-block;
}
.save:hover{
    opacity: 0.7;
}
.block_with_registr .input_for_title:focus {
    outline: none;
}
textarea::placeholder {
  color:rgba(255, 255, 255, 0.5);
}
input::placeholder {
    color:rgba(255, 255, 255, 0.5);
  }
textarea:focus {
    outline: none;
}
.line{
    color:#BBC4DB;
    margin-top: 20px;
}
.text_under_line{
    font-family: 'ClearSans-Light';
    color:white;
    margin: 0px 3%;
}
.info_about_writer{
   padding: 2% 0px;
}
.save:target{
    visibility:visible;
}
.input_for_title:focus {
    outline: none;
}
.space_for_note_edit_and_show{
    padding-top: 2%;
    background-color: #617299;
    width:60%;
    border-radius: 10px;
    margin-top: 70px;
    margin-left: 10%;
    height: auto;
    z-index: 10;
    overflow-y: auto;
    overflow-x: hidden;
    display: inline-block;
}
.space_for_note_edit_and_show i{
    color: white;
    font-size: 120%;
}
.button_back_to_all_notes{
    font-size: 230%;
    font-weight: bold;
    text-decoration: none;
    border:none;
    color: #F1F7ED;
    display: inline-block;
    margin-left: 3%;
    cursor: pointer;
}
.space_for_note_edit_and_show .content .comment{
    font-size:110%;
    font-family: 'ClearSans-Regular';
    background-color: #617299;
    border:none;
    color:white;
    width: 100%;
    min-height: 50px;
    resize: none;
    width: 94%;
    margin: 0px 5% 0px 3%;
}
.space_for_note_edit_and_show .textarea_for_link{
    font-family: 'ClearSans-Light';
    color:white;
    background-color: rgba(43, 59, 95, 0.75);
    text-align:left;
    padding: 10px;
    border-radius: 8px;
    font-size: 20px;
    color: #F1F7ED;
    width: 75%;
    border:none;
    resize: none;
    height: 50px;
    min-height: 50px;
    cursor: pointer;
    margin: 20px 4% 1vw 2%;
    display: inline-block;
}
.space_for_note_edit_and_show.textarea_for_link:focus{
    outline:none ;
}
.space_for_note_edit_and_show .info_about_writer{
    display: flex;
    flex-direction: column;
    align-self: flex-end;
}

</style>
