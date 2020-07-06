/**
 * Скрипт таймера.
 * Пользователь добавляет\убавляет минуты\секунды для получения желаемого времени. При нажатии кнопки 'start'
 * программа производит обратный отсчет. При завершении отсчета выводится сообщение 'Время истекло!'.
 * При нажатии кнопки 'stop'отсчет прекращается и выводится сообщение 'Время истекло!'. При нажатии кнопки
 * 'reset' скрипт перезапускается для нового осчета.
 */
const timer = document.querySelector('.countdown');
const minutes = document.querySelector('.minutes');
const seconds = document.querySelector('.seconds');
const message = document.querySelector('.message');

const plus_one_min = document.querySelector('.plus-one-min');
const plus_five_min = document.querySelector('.plus-five-min');
const plus_ten_min = document.querySelector('.plus-ten-min');
const minus_one_min = document.querySelector('.minus-one-min');
const minus_five_min = document.querySelector('.minus-five-min');
const minus_ten_min = document.querySelector('.minus-ten-min');

const plus_one_sec = document.querySelector('.plus-one-sec');
const plus_five_sec = document.querySelector('.plus-five-sec');
const plus_ten_sec = document.querySelector('.plus-ten-sec');
const minus_one_sec = document.querySelector('.minus-one-sec');
const minus_five_sec = document.querySelector('.minus-five-sec');
const minus_ten_sec = document.querySelector('.minus-ten-sec');

const start = document.querySelector('.start');
const stop_ = document.querySelector('.stop');
const reset = document.querySelector('.reset');

var countSec = 0; //содержит отсчитываемое время

const updateText = () =>{ //обновляет текст, показывающий минуты и секунды таймера
  minutes.innerHTML = Math.floor(countSec / 60) ;
  seconds.innerHTML = countSec - minutes.innerHTML * 60;
}

const countDown = () => {	//производит обратный отсчет заданного времени
    const timeinterval = setTimeout(countDown, 1000);
    if (countSec <= 0) {
      clearInterval(timeinterval);
      timer.style.display = 'none';
      message.innerHTML = '<p>Время истекло!</p>'
    }
    if(countSec > 0) countSec--;
    updateText();
}


// функции добавляющие и убавляющие минуты
plus_one_min.onclick = () =>{
    countSec += 60;
    if(countSec > 3599) {
        countSec = 3599;
    }
    updateText()
}

plus_five_min.onclick = () =>{
    countSec += 300;
    if(countSec > 3599) {
        countSec = 3599;
    }
    updateText()
}

plus_ten_min.onclick = () =>{
    countSec += 600;
    if(countSec > 3599) {
        countSec = 3599;
    }
    updateText()
}

minus_one_min.onclick = () =>{
    countSec -= 60;
    if(countSec < 0) {
        countSec = 0;
    }
    updateText()
}

minus_five_min.onclick = () =>{
    countSec -= 300;
    if(countSec < 0) {
        countSec = 0;
    }
    updateText()
}

minus_ten_min.onclick = () =>{
    countSec -= 600;
    if(countSec < 0) {
        countSec = 0;
    }
    updateText()
}

// функции добавляющие и убавляющие секунды
plus_one_sec.onclick = () =>{
    countSec += 1;
    if(countSec > 3599) {
        countSec = 3599;
    }
    updateText()
}

plus_five_sec.onclick = () =>{
    countSec += 5;
    if(countSec > 3599) {
        countSec = 3599;
    }
    updateText()
}

plus_ten_sec.onclick = () =>{
    countSec += 10;
    if(countSec > 3599) {
        countSec = 3599;
    }
    updateText()
}

minus_one_sec.onclick = () =>{
    countSec -= 1;
    if(countSec < 0) {
        countSec = 0;
    }
    updateText()
}

minus_five_sec.onclick = () =>{
    countSec -= 5;
    if(countSec <0) {
        countSec = 0;
    }
    updateText()
}

minus_ten_sec.onclick = () =>{
    countSec -= 10;
    if(countSec < 0) {
        countSec = 0;
    }
    updateText()
}

//функции управления
start.onclick = () => { //запускает обратный отсчет таймера
	  countDown();  
}

stop_.onclick = () => { //останавливает обратный отсчет таймера
    countSec = 0;  
}

reset.onclick = () => { //перезапускает таймер обратный отсчет таймера
    location.reload()  
}