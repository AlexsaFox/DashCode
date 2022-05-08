<template>
  <div class="block">
    <div class="avatar">
      <a href="#popup4">
        <img src="../../../src/assets/img/205d9582975737a8b02fb1e5bbc02fd5.jpg" class="avatar" alt="Avatar">
      </a>
    </div>
    <div class="text">
      <span>user.username</span>
    </div>
    <div class="display_with_button">
      <a href="#popup"><button class="standard_button">
        <div class="i-carbon:add" />Add notes
      </button></a>
      <a><button class="standard_button">
        <div class="i-carbon:arrow-right" />Social media
      </button></a>
      <a><button class="standard_button">
        <div class="i-carbon:user-avatar-filled-alt" /> Subscritions
      </button></a>
      <a href="#popup5"><button class="standard_button">
        <div class="i-carbon:folder" />My notes
      </button></a>
    </div>
  </div>
  <div id="popup4" class="overlay">
    <div class="profile_popup">
      <div class="header_for_pop_up">
        user.name
        <a class="close" href="#">&times;</a>
      </div>
      <hr>
      <div class="content" style="padding: 10px;">
        <span><a href="/user/settings">Settings</a></span>
        <br>
        <span><a href="/auth/logout">Log out</a></span>
      </div>
    </div>
  </div>
  <div id="popup5" class="overlay_1">
    <div class="my_notes_popup">
      <div class="header_for_pop_up_acc">
        All your notes:
        <a class="close" href="#">&times;</a>
      </div>
      <div class="content">
        <ul
          style=" list-style-type: none;
                max-height: 350px;
                overflow-y: auto"
        >
          <!-- {% for note in notes %} -->
          <li style="height: 30px;line-height: 30px;">
            <a href="note.id">note.title</a>
          </li>
          <!-- {% endfor %} -->
        </ul>
      </div>
    </div>
  </div>
</template>
<style scoped lang="scss">
@import "../../assets/scss/standard-button.scss";
.standard_button{
  @include standard-button;
}
.block{
    color:white;
    font-family: 'ClearSans-Regular';
    display: inline-block;
    position: fixed;
    width: 20%;
    right: 15px;
    top:40px;

}
.text{
    position: absolute;
    top:40px;
    left: 150px;
    display: inline-block;
    font-size:140%;
}
.avatar {
    position: relative;
    overflow:hidden;
    width:100px;
    height:100px;
    display: inline-block;
    margin-bottom: 10%;
    margin-left: 2%;
}

.avatar img {
    border-radius: 50%;
    position: absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    width:100px;
    height:100px;
    display: inline-block;
    object-fit:cover;
}
.display_with_button div{
    color: #F1F7ED;
}
.display_with_button button{
    width:100%;
}
.b_my_notes:focus{
    background-color: var(--primary-color);
}
.display_with_button{
    display: inline-block;
    width:100%;
}
.overlay {
    position: fixed;
    top: -20px;
    bottom: 0;
    left: 0;
    right: 0.8vw;
    transition: opacity 500ms;
    visibility: hidden;
    opacity: 0;
    height: 100%;
    z-index: 10;

}
.overlay:target {
    visibility: visible;
    opacity: 1;
    overflow:none;
}
.profile_popup{
   margin: 70px auto;
   background: #09132B;
   border-radius: 10px;
   width: 20.2%;
   position: relative;
   top:-3.4%;
   left:39.69%;
   padding-top: 20px;
   color:white;
   .header_for_pop_up{
   font-family: 'ClearSans-Regular';
   color:white;
   background-color: #09132B;
   text-align:left;
   padding: 10px;
   border-radius: 10px;
   font-size: 20px;
   margin: 0px 6% 0px 4%;
   color: #F1F7ED;
   overflow: hidden;
  text-overflow: ellipsis;
}
.close {
 position: absolute;
 top: 20px;
 right: 20px;
 transition: all 200ms;
 font-size: 120%;
 font-weight: bold;
 text-decoration: none;
 color: #F1F7ED;
}
.close:hover {
 color: #303D67;
}
.content {
   text-align: left;
   font-family: 'ClearSans-Regular';
   color:white;
   padding: 0px 3%;
   max-height: 40%;
   overflow: auto;
   margin-left: 4%;
   background-color: #09132B;
   border-radius: 0 0 10px 10px;
}
.header_for_pop_up_acc{
    display: flex;
    font-family: 'ClearSans-Regular';
    color:white;
    background-color: #303D67;
    text-align:right;

    padding: 10px;
    border-radius: 10px;
    font-size: 20px;
    margin: 0px 60px 20px 20px;
    color: #F1F7ED;
}
}
.overlay_1 {
    position: fixed;
    top:90px;
    bottom: 0;
    left: 0;
    right: 15px;
    transition: opacity 500ms;
    visibility: hidden;
    opacity: 0;
    height: 100%;
    z-index: 10;

}
.overlay_1:target {
    visibility: visible;
    opacity: 1;
}
.my_notes_popup{
   margin: 70px auto;
   background: #303D67;
   border-radius: 10px;
   width: 20.5%;
   position: relative;
   top:29%;
   left:39.8%;
   padding-top: 20px;
  .header_for_pop_up{
    display: flex;
    font-family: 'Altone-SemiBold';
    color:white;
    background-color: #303D67;
    text-align:left;

    padding: 10px;
    border-radius: 10px;
    font-size: 20px;
    margin: 0px 60px 20px 20px;
    color: #F1F7ED;
  }
  .close {
    position: absolute;
    top: 20px;
    right: 20px;
    transition: all 200ms;
    font-size: 190%;
    font-weight: bold;
    text-decoration: none;
    color: #F1F7ED;
  }
  .close:hover {
    color: #09132B;
  }
  .content {
    text-align: left;
    font-family: 'ClearSans-Regular';
    color:white;
    padding: 0px 3%;
    height: 10%;
    overflow: auto;
    background-color: #303D67;
    border-radius: 0 0 10px 10px;

  }

  .header_for_pop_up_acc{
      display: flex;
      font-family: 'ClearSans-Regular';
      color:white;
      background-color: #303D67;
      text-align:right;

      padding: 10px;
      border-radius: 10px;
      font-size: 20px;
      margin: 0px 60px 20px 20px;
      color: #F1F7ED;
  }
}

</style>
