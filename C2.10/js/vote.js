const btnCats = document.getElementById('vote-cats');
btnCats.addEventListener('click', async _ => {
    const response = await fetch('https://sf-pyw.mosyag.in/sse/vote/cats', {
        method: 'post'
    });
});

const btnDogs = document.getElementById('vote-dogs');
btnDogs.addEventListener('click', async _ => {
    const response = await fetch('https://sf-pyw.mosyag.in/sse/vote/dogs', {
        method: 'post'
    });
});

const btnParrots = document.getElementById('vote-parrots');
btnParrots.addEventListener('click', async _ => {
    const response = await fetch('https://sf-pyw.mosyag.in/sse/vote/parrots', {
        method: 'post'
    });
});

const btnVoteResults = document.getElementById('vote-result');
console.log(btnVoteResults);
btnVoteResults.addEventListener('click', async _ => {
    console.log('button press');
    window.open("result.html");
});