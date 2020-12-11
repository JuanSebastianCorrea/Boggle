let score = 0;
let words = new Set();
let secs = 85;
let clearID;

$('document').ready(show_timer);
$('#start-btn').on('click', function() {
	timer();
	$('#enter-btn').toggleClass('hidden');
	$('#word').toggleClass('hidden');
	$('#word').focus();
	$('#start-btn').hide();
});

$('.add-word').on('submit', handleSubmit);
$('#restart-btn').on('click', function() {
	location.reload();
});

async function handleSubmit(evt) {
	evt.preventDefault();
	let $word = $('#word');
	let word = $word.val();

	if (!word) return;

	if (words.has(word)) {
		show_message(`${word} was already found!`);
		return;
	}

	let response = await axios.get('/check-word', { params: { word: word } });
	// console.log(response);

	if (response.data.result === 'not-on-board') {
		show_message(`${word} is not a word on this board`);
	} else if (response.data.result === 'not-word') {
		show_message(`${word} is not a valid english word`);
	} else {
		words.add(word);
		show_word(word);
		score += word.length;
		show_score(score);
		show_message(`Added: ${word}`);
	}
	$word.val('');
}

function show_message(msg) {
	$('#msg').text(msg);
}

function show_score(score) {
	$('#score').text(score);
}

function show_word(word) {
	$('#words').append(`<li class="list-group-item">${word}</li>`);
}

function show_timer() {
	$('#timer').text(secs);
}

function timer() {
	clearID = setInterval(tick, 1000);
}

async function tick() {
	secs -= 1;
	show_timer();

	if (secs === 0) {
		clearInterval(clearID);
		await scoreGame();
	}
}

async function scoreGame() {
	$('.add-word').hide();
	$('#start-btn').hide();
	$('#restart-btn').toggleClass('hidden');
	const res = await axios.post('/post-score', { score: score });
	console.log(res);

	if (res.data.brokeRecord) {
		show_message(`New record: ${score}`);
		$('#high-score').text(score);
		if (plays === 1) {
			$('#num-plays').html('<i> (in 1 play) </i>');
		} else {
			$('#num-plays').html(`<i> (in ${plays} plays) </i>`);
		}
	} else {
		show_message(`Final score: ${score}`);
		$('#num-plays').html(`<i> (in ${plays} plays) </i>`);
	}
}
