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

        questionInput.value = ''; // Clear input field
        answerInput.value = ''; // Clear input field
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
        document.getElementById('addMoreButton').style.display = 'inline'; // Show the add more button
    }
});

document.getElementById('addMoreButton').addEventListener('click', function() {
    document.getElementById('cardInput').style.display = 'block'; // Show input fields
    document.getElementById('flashcard').style.display = 'none'; // Hide the flashcard
    document.getElementById('flipButton').style.display = 'none'; // Hide the flip button
    document.getElementById('nextButton').style.display = 'none'; // Hide the next button
    document.getElementById('addMoreButton').style.display = 'none'; // Hide the add more button
});

document.getElementById('flipButton').addEventListener('click', function() {
    document.getElementById('flashcard').classList.toggle('flipped');
});

document.getElementById('nextButton').addEventListener('click', function() {
    currentCardIndex = (currentCardIndex + 1) % flashcards.length;
    if(currentCardIndex === 0) { // Optionally, hide or show the addMoreButton when the last card is reached again
        document.getElementById('addMoreButton').style.display = 'inline';
    }
    updateFlashcard();
});

function updateFlashcard() {
    const card = flashcards[currentCardIndex];
    const flashcardDiv = document.getElementById('flashcard');
    flashcardDiv.classList.remove('flipped'); // Reset to front side
    flashcardDiv.querySelector('.front').textContent = card.question;
    flashcardDiv.querySelector('.back').textContent = card.answer;
}
