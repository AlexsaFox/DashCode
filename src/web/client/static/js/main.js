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


// обновление цвета




const dynamicInputs = document.querySelectorAll('input.input-color-picker');

const handleThemeUpdate = (cssVars) => {
    const root = document.querySelector(':root');
    const keys = Object.keys(cssVars);
    keys.forEach(key => {
        root.style.setProperty(key, cssVars[key]);
    });
}


dynamicInputs.forEach((item) => {
    item.addEventListener('input', (e) => {
        handleThemeUpdate({
            [`--primary-color`]: e.target.value
        });
    });
});
function fnOC(){
    let elem1=document.querySelector('#comment');
    elem1.readOnly=false;
    let elem2=document.querySelector('#code');
    elem2.readOnly=false;
    let elem3=document.querySelector('#textarea_for_tegs');
    elem3.readOnly=false;
    let elem4=document.querySelector('#textarea_for_link');
    elem4.readOnly=false;
    let elem = document.querySelector('#input_for_title');
    elem.disabled = false;
    document.getElementById('save').style.visibility="visible";
}
function fnSave(){
    let elem1=document.querySelector('#comment');
    elem1.readOnly=true;
    let elem2=document.querySelector('#code');
    elem2.readOnly=true;
    let elem3=document.querySelector('#textarea_for_tegs');
    elem3.readOnly=true;
    let elem4=document.querySelector('#textarea_for_link');
    elem4.readOnly=true;
    let elem = document.querySelector('#input_for_title');
    elem.disabled = true;
    document.getElementById('save').style.visibility="visible";
    document.getElementById('save').style.visibility="hidden";
    
}