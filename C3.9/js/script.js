if (getCookie('city') != true) {
    console.log('block undefined')
    let inp = document.querySelector('#city-name');
    inp.remove();

    let p = document.createElement('p');
    p.innerHTML = 'Ваш город — ' + getCookie('city');
    document.body.append(p);

    let btnRem = document.createElement('button');
    btnRem.innerHTML = 'Удалить город';
    document.body.append(btnRem);
    
    btnRem.addEventListener('click', async _ => {
        deleteCookie('city');
    });
} else {
    console.log('block defined')

    let inp = document.querySelector('#city-name');
    inp.oninput = () => {
        setCookie('city', inp.value, {
            'max-age': 3600 // cookie live 10 min
        })
    };
}

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
   return matches ? decodeURIComponent(matches[1]) : undefined;
}

function setCookie(name, value, options = {}) {

    options = {
        path: '/',
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

function deleteCookie(name) {
    setCookie(name, "", {
        'max-age': -1
    })
}  

