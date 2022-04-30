function openSettings(evt, settings) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("standart_button");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(settings).style.display = "block";
    evt.currentTarget.className += " active";
}

function editPassword(evt) {
    
    document.getElementById('button_change_password').style.display = "none";
    document.getElementById('new_password_container').style.display = "flex";
    document.getElementById('confirm_password_container').style.display = "flex";

    editAccount();
}

function editEmail(evt, input_type) {

    document.getElementById(input_type).disabled = false;

    evt.target.style.display = "none";

    editAccount();
}

function editAccount() {
    
    document.getElementById('current_password_container').style.display = "flex";
    document.getElementById('edit_account_settings').style.display = "flex";
}

function editUsername(evt, input_type) {
    document.getElementById(input_type).disabled = false;

    evt.target.style.display = "none";

    document.getElementById('edit_username').style.display = "flex";
}

// copy API token

function copyToken(evt) {
    window.navigator.clipboard.writeText(document.getElementById('API_token').value);
}


//
function fnOC(){
    let elem1=document.querySelector(".comment");
    elem1.readOnly=false;
    let elem2=document.querySelector(".code");
    elem2.readOnly=false;
    let elem3=document.querySelector(".textarea_for_tegs");
    elem3.readOnly=false;
    let elem4=document.querySelector(".textarea_for_link");
    elem4.readOnly=false;
    let elem = document.querySelector(".input_for_title");
    elem.disabled = false;
}
function fnSave(){
    let elem1=document.querySelector(".comment");
    elem1.readOnly=true;
    let elem2=document.querySelector(".code");
    elem2.readOnly=true;
    let elem3=document.querySelector(".textarea_for_tegs");
    elem3.readOnly=true;
    let elem4=document.querySelector(".textarea_for_link");
    elem4.readOnly=true;
    let elem = document.querySelector(".input_for_title");
    elem.disabled = true;
    
}

window.onload = () => {
    let tx = document.querySelectorAll("textarea");
    console.log(tx);
    for (const textarea of tx) {
    console.log(textarea);
    textarea.setAttribute("style", "height:" + (textarea.scrollHeight) + "px;overflow-y:hidden;");
    textarea.addEventListener("input", OnInput, false);
    }
}

function OnInput() {
  this.style.height = "auto";
  this.style.height = (this.scrollHeight) + "px";
}