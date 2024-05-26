$(document).ready(function() {
    $('#generateImageBtn').click(function() {
        $.ajax({
            url: 'http://127.0.0.1:8000/get-image',
            type: 'GET',
            success: function(response) {
                $('#generatedImage').attr('src', response.imageUrl);
                $('#hintsList').empty();
                $('#hintsList').text('Hints: ' + response.hints.join(', '));
                $('#imageContainer').removeClass('hidden');
                $('#generateImageBtn').addClass('hidden'); // Hide button after generating image
            },
            error: function() {
                alert('Failed to generate image and hints. Please try again.');
            }
        });
    });

    $('#submitGuessBtn').click(function() {
        const originalPromptText = $('#hintsList').text().replace('Hints: ', '');
        const guessedPrompt = $('#guessedPrompt').val();

        $.ajax({
            url: 'http://127.0.0.1:8000/get-score',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ originalPrompt: originalPromptText, guessedPrompt }),
            success: function(response) {
                $('#similarityScore').text(response.score);
                $('#guessedImage').attr('src', response.generatedImage);
                
                // Show original prompt below the generated image
                $('#originalPrompt').text('Original Prompt: ' + originalPromptText);
                $('#originalPrompt').removeClass('hidden');
                
                // Show guessed prompt below the guessed image
                $('#guessedPromptText').text('Guessed Prompt: ' + guessedPrompt);

                $('#hintGuessContainer').replaceWith($('#resultContainer')); // Replace hint-guess-container with resultContainer
                $('#resultContainer').removeClass('hidden');
            },
            error: function() {
                alert('Failed to get similarity score. Please try again.');
            }
        });
    });
});
