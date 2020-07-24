var btn = document.querySelector('#save');
var btnDel = document.querySelector('#del-all');

var chbNotCall = document.getElementById('not-call');
var chbIReadIt = document.getElementById('I-read-it');
var chbIDontChoose = document.getElementById("I-dont-choose");
var chbIConfirm = document.getElementById('I-confirm');
var chbImOver = document.getElementById("Im-over-12-years-old");
var chbThisTask = document.getElementById('this-task-is-completed');

if (getCookie('poll')) { //if the poll on this page has already taken place
    setCondition(chbNotCall);
    setCondition(chbIReadIt);
    setCondition(chbIDontChoose);
    setCondition(chbIConfirm);
    setCondition(chbImOver);
    setCondition(chbThisTask);
    
    btn.disabled = true;
}

btn.addEventListener('click', async _ => {
    date = getLifetime();

    setCookie('poll', 1, {
        expires: date,
    })

    saveState(chbNotCall);
    saveState(chbIReadIt);
    saveState(chbIDontChoose);
    saveState(chbIConfirm);   
    saveState(chbImOver);
    saveState(chbThisTask);
    
    btn.disabled = true;
});

btnDel.addEventListener('click', async _ => {
    deleteAllCookies();
});

function setCondition(name) {
    //This function restores condition of checkboxes on startup p
    var temp = document.getElementById(name.id);
    if(getCookie(name.id) == 1) {
        temp.checked = true;
    }
    temp.disabled = true;
}

function getLifetime() {
    let date = new Date(Date.now() + 86400e3); //the lifetime of cookies one day
    return date.toUTCString();
}

function saveState (name) { //accepts a variable with the checkbox as an argument
    //This function saves the state using coockies
    date = getLifetime();

    if(name.checked) {
        let nameCoockie = name.id;
        setCookie(nameCoockie, 1, {
            expires: date,
        })
    } else {
        let nameCoockie = name.id;
        setCookie(nameCoockie, 0, {
            expires: date,
        })
    }
    
    name.disabled = true;  
}

function getCookie(name) {
    //This function get coockie with name "name"
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

function setCookie(name, value, options = {}) {
    //This function set coockie
    options = {
        path: '/',
        ...options
    };

    if (options.expires.toUTCString) {
        options.expires = options.expires.toUTCString();
    }

    let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);
    for (let optionKey in options) {
        updatedCookie += "; " + optionKey;
        let optionValue = options[optionKey];
        if (optionValue !== true) {
        updatedCookie += "=" + optionValue;
        }
    }
    document.cookie = updatedCookie;
}

function deleteAllCookies() {
    //This function delet all coockies and make all checkboxes is unchecked
    document.cookie.split(";").forEach(function(c) {
        document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); });
    
    chbNotCall.checked = false;
    chbIReadIt.checked = false;
    chbIDontChoose.checked = false;
    chbIConfirm.checked = false;
    chbImOver.checked = false;
    chbThisTask.checked = false;
    
    btn.disabled = false;
}