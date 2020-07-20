const progressCat = document.querySelector('.progress-cat');
const progressDog = document.querySelector('.progress-dog');
const progressParrot = document.querySelector('.progress-parrot');

const header = new Headers({
    'Access-Control-Allow-Credentials': true,
    'Access-Control-Allow-Origin': '*'
})

const url = new URL('https://sf-pyw.mosyag.in//sse/vote/stats')
const ES = new EventSource(url, header)

ES.onerror = error => {
    ES.readyState ? progressCat.textContent = "Some error" : null;
}

ES.onmessage = message => {
    obj = JSON.parse(message.data);
    sum = obj.cats + obj.parrots + obj.dogs;
    
    catPercent =  Math.round(obj.cats * 100 / sum);
    progressCat.style.cssText = `width: ${catPercent}%;`;
    progressCat.textContent = `${catPercent}%`;

    dogPercent =  Math.round(obj.dogs * 100 / sum);
    progressDog.style.cssText = `width: ${dogPercent}%;`;
    progressDog.textContent = `${dogPercent}%`;

    parrotPercent =  Math.round(obj.parrots * 100 / sum);
    progressParrot.style.cssText = `width: ${parrotPercent}%;`;
    progressParrot.textContent = `${parrotPercent}%`;
}
