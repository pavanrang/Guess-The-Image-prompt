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
                $('#guessContainer').removeClass('hidden');
            },
            error: function() {
                alert('Failed to generate image and hints. Please try again.');
            }
        });
    });

    $('#submitGuessBtn').click(function() {
        const originalPrompt = $('#hintsList').text();
        const guessedPrompt = $('#guessedPrompt').val();

        $.ajax({
            url: 'http://127.0.0.1:8000/get-score',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ originalPrompt, guessedPrompt }),
            success: function(response) {
                $('#similarityScore').text(response.score);
                $('#guessedImage').attr('src', response.generatedImage);
                $('#resultContainer').removeClass('hidden');
            },
            error: function() {
                alert('Failed to get similarity score. Please try again.');
            }
        });
    });
});