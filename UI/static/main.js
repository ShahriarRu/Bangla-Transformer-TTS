document.addEventListener('DOMContentLoaded', () => {
    const textInput = document.getElementById('text_input');
    const generateButton = document.getElementById('generate_button');
    const successMessage = document.getElementById('success_message');
    const playButton = document.getElementById('play_button');
    const audioPlayer = document.getElementById('audio_player');

    generateButton.addEventListener('click', () => {
        const text = textInput.value;

        // Send the text to the backend for audio generation
        fetch('/synthesize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text }),
        })
        .then(response => response.json())
        .then(data => {
            // Reset the audio player and success message
            audioPlayer.pause();
            audioPlayer.currentTime = 0;
            audioPlayer.style.display = 'none';
            successMessage.textContent = '';
            successMessage.style.display = 'none';

            // Display the success message and show the play button
            successMessage.textContent = 'Audio generated successfully!';
            successMessage.style.display = 'block';
            playButton.style.display = 'block';

            // Store the audio URL in the play button's data attribute
            playButton.dataset.audioUrl = data.audio_url;
        })
        .catch(error => {
            console.error('Error generating audio:', error);
        });
    });

    playButton.addEventListener('click', () => {
        // Get the audio URL from the play button's data attribute
        const audioUrl = playButton.dataset.audioUrl;

        // Fetch the audio file using the audio URL
        fetch(audioUrl)
        .then(response => response.blob())
        .then(blob => {
            // Create a blob URL from the fetched audio blob
            const blobUrl = URL.createObjectURL(blob);

            // Set the audio player source to the blob URL and play the audio
            audioPlayer.src = blobUrl;
            audioPlayer.style.display = 'block';
            audioPlayer.play();
        })
        .catch(error => {
            console.error('Error fetching audio:', error);
        });
    });
});
