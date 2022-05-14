<template>
  <div id="popup_check" class="overlay">
    <div class="popup_check">
      <div class="header_for_pop_up">
        <a class="close" href="#">&times;</a>
      </div>
      <div class="content">
        <span>Do you want to save your changes?</span>
        <div class="buttons_for_check">
          <div class="each_button_for_popup_check">
            <a href="#"><input type="button" value="Unsave"></a>
          </div>
          <div class="each_button_for_popup_check">
            <a href="#"><input type="button" value="Save"></a>
          </div>
          <div class="each_button_for_popup_check">
            <a href="#popup_watch"><input
              type="button"
              value="Cancel"
            ></a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style>
.overlay {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(0, 0, 0, 0.7);
    transition: opacity 500ms;
    visibility: hidden;
    opacity: 0;
    height: 100%;
    z-index: 10;
    overflow-y: auto;
}
.overlay:target {
    visibility: visible;
    opacity: 1;
    overflow:none;
}

.popup_check {
    margin: 70px auto;
    background: #5B6B98;
    border-radius: 10px;
    width: 30%;
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
.popup_check .content{
    font-family:'ClearSans-Light';
    text-align: center;
    color:white;
    font-size: 120%;

}
.popup_check .buttons_for_check input{
    font-size: 80%;
    font-family:'ClearSans-Light';
    background-color: #86faf8;
    color:#223153;
    border-radius: 5px;
    border: none;
    margin: 5% 2% 0px;
    padding: 0px 15%;
}
.popup_check .buttons_for_check{
    margin:5% 0px;
    padding-bottom: 2%;
}
.each_button_for_popup_check{
    display: inline-block;
    width: 20%;
}

</style>
