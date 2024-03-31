let flashcards = [];
let currentCardIndex = 0;

document.getElementById('addButton').addEventListener('click', function() {
    const questionInput = document.getElementById('questionInput');
    const answerInput = document.getElementById('answerInput');
    
    if (questionInput.value && answerInput.value) {
        flashcards.push({
            question: questionInput.value,
            answer: answerInput.value
        });

        questionInput.value = '';
        answerInput.value = '';
    } else {
        alert("Please enter both a question and an answer.");
    }
});

document.getElementById('endButton').addEventListener('click', function() {
    document.getElementById('cardInput').style.display = 'none';
    if (flashcards.length > 0) {
        updateFlashcard();
        document.getElementById('flashcard').style.display = 'block';
        document.getElementById('flipButton').style.display = 'inline';
        document.getElementById('nextButton').style.display = 'inline';
        document.getElementById('addMoreButton').style.display = 'inline';
    }
});

document.getElementById('addMoreButton').addEventListener('click', function() {
    document.getElementById('cardInput').style.display = 'block';
    document.getElementById('flashcard').style.display = 'none';
    document.getElementById('flipButton').style.display = 'none';
    document.getElementById('nextButton').style.display = 'none';
    document.getElementById('addMoreButton').style.display = 'none';
});

document.getElementById('flipButton').addEventListener('click', function() {
    document.getElementById('flashcard').classList.toggle('flipped');
});

document.getElementById('nextButton').addEventListener('click', function() {
    currentCardIndex = (currentCardIndex + 1) % flashcards.length;
    if(currentCardIndex === 0) {
        document.getElementById('addMoreButton').style.display = 'inline';
    }
    updateFlashcard();
});

function updateFlashcard() {
    const card = flashcards[currentCardIndex];
    const flashcardDiv = document.getElementById('flashcard');
    flashcardDiv.classList.remove('flipped');
    flashcardDiv.querySelector('.front').textContent = card.question;
    flashcardDiv.querySelector('.back').textContent = card.answer;
}
