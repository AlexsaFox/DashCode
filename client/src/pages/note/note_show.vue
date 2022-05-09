<script setup lang="ts">
const { t } = useI18n()
</script>
<template>
  <div class="overlay_for_space_for_note_edit_and_show">
    <div class="space_for_note_edit_and_show">
      <input value="note.title" class="input_for_title" disabled>
      <!-- {% if note.is_private == True %} -->
      <div class="button_status">
        <span><div class="i-carbon:unlocked" /></span>
      </div>
      <!-- {% else %}
      <div class="button_status">
        <span><i class="bx bx-lock-open-alt" /></span>
      </div>
      {% endif %} -->
      <button onclick="location.href='{{ url_for('webapp.index.index_view') }}'" class="button_back_to_all_notes">
        <div class="i-carbon:close" />
      </button>
      <div class="content">
        <div class="div_for_comment">
          <TextareaAutosize :min-height="50" class="comment" readonly>
            По широкой, обсаженной деревьями, большой бесшоссейной дороге, слегка погромыхивая рессорами, шибкою рысью ехала высокая голубая венская коляска цугом. За коляской скакали свита и конвой кроатов. Подле Кутузова сидел австрийский генерал в странном, среди черных русских, белом мундире. Коляска остановилась у полка. Кутузов и австрийский генерал о чем-то тихо говорили, и Кутузов слегка улыбнулся, в то время как, тяжело ступая, он опускал ногу с подножки, точно как будто и не было этих двух тысяч людей, которые не дыша смотрели на него и на полкового командира.
            Раздался крик команды, опять полк звеня дрогнул, сделав на караул. В мертвой тишине послышался слабый голос главнокомандующего. Полк рявкнул: «Здравья желаем, ваше го-го-го-ство!» И опять все замерло. Сначала Кутузов стоял на одном месте, пока полк двигался; потом Кутузов рядом с белым генералом, пешком, сопутствуемый свитою, стал ходить по рядам.
          </TextareaAutosize>
        </div>
        <!-- (class_="comment",placeholder="text",cols="80", rows="11") -->
        <a><textarea class="textarea_for_link" readonly>note.link</textarea></a>
        <!-- (class_="textarea_for_link",placeholder="htts://",cols="90", rows="1") -->

        <a href="{{url_for('webapp.note.notes_edit', note_id=id)}}"><input
          type="submit" class="save"
          :value="t('note_show.edit-button')"
        ></a>
        <hr class="line">
        <div class="info_about_writer">
          <span class="text_under_line">{{ t("note_show.author-of-note") }}: note.user.username</span>
          <span class="text_under_line">{{ t("note_show.date-of-creation-label") }}: note.creation_date.strftime</span>
        </div>
      </div>
    </div>
  </div>
  <NavButtons />
</template>
<style>
.input_for_title{
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
.button_status{
    font-size: 130%;
    display: inline-block;
    margin-left: 1%;
}
.button_status div{
    color:white;
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
.button_delite:hover{
    opacity: 0.7;
}
.buttons_in_the_bottom{
    display: inline-block;
    width: 20%;
}
.input_for_title:focus {
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

.button_back_to_all_notes{
    font-size: 230%;
    font-weight: bold;
    text-decoration: none;
    border:none;
    color: #F1F7ED;
    display: inline-block;
    margin-left: 6%;
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
    width: 100%;
}
.div_for_comment{
    width: 94%;
    margin-left: 3%;
    overflow: hidden;
    text-overflow: ellipsis;
    color: white;
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
