
function jQuery (selector, context = document){
	this.elements = Array.from(context.querySelectorAll(selector));
	return this
}

jQuery.prototype.each = function (fn){
	this.elements.forEach((element, index) => fn.call(element, element, index));
	return this;
}

//метод jQuery.prototype.html() возвращает или изменяет html-содержимое выбранных элементов.
jQuery.prototype.html = function(txt_cont = null) {
    if (txt_cont === null) {
        console.log('return elem'); //Служит для проверки работы
        return this;
    } else {
        this.each(element => element.innerHTML = txt_cont);
        return this;
    }
}
//метод jQuery.prototype.text() возвращает или изменяет текстовое содержимое выбранных элементов.
jQuery.prototype.text = function(txt_cont = null) {
    if (txt_cont === null) {
        console.log('return elem'); //Служит для проверки работы
        return this;
    } else {
        this.each(element => element.textContent = txt_cont);
        return this;
    }
}

const $ = (e) => new jQuery(e);

//Проверка путем замены элемента. Разкомментируй строку.
//$('b').html('<i>jMyQuery</i>');
//$().html();

//Проверка путем замены текста jQuery на jMyQuery. Разкомментируй строку.
//$('b').text('jMyQuery'); //с аргументами изменяет jQuery на jMyQuery и возвращает измененного себя
//$().text();  //без аргументов возвращает себя
