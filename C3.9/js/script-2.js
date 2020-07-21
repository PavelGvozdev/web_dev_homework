if (localStorage.getItem('city')) {
    let inp = document.getElementsByClassName('js-city');
    inp.remove();

    let p = document.createElement('p');
    p.innerHTML = 'Ваш город — Архангельск';
    document.body.append(p);

    let btnRem = document.createElement('button');
    btnRem.innerHTML = 'Удалить город';
    
    btnRem.addEventListener('click', async _ => {
        localStorage.removeItem('city');
    });
} 


js-city.oninput = () => {
    localStorage.setItem('city', js-city.value)
};