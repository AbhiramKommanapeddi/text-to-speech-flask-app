const textInput = document.getElementById('text-input');
const languageSelect = document.getElementById('language-select');
const convertButton = document.getElementById('convert-button');
const audioPlayer = document.getElementById('audio-player');
const statusMessage = document.getElementById('status-message');

convertButton.addEventListener('click', async () => {
    const text = textInput.value.trim();
    const lang = languageSelect.value;

    if (text === '') {
        statusMessage.textContent = 'Please enter some text to convert.';
        audioPlayer.style.display = 'none';
        return;
    }

    statusMessage.textContent = 'Converting...';
    convertButton.disabled = true; // Disable button during conversion
    audioPlayer.style.display = 'none'; // Hide audio player until new audio is ready
    audioPlayer.src = ''; // Clear previous audio

    try {
        const response = await fetch('/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text, lang: lang }),
        });

        const result = await response.json();

        if (response.ok) {
            const audioUrl = result.audio_url; // Get the URL from the Flask response
            audioPlayer.src = audioUrl;
            audioPlayer.style.display = 'block'; // Show the audio player
            audioPlayer.play(); // Automatically play the audio
            statusMessage.textContent = 'Conversion successful. Playing audio...';
        } else {
            statusMessage.textContent = `Error: ${result.error || 'Unknown error from server'}`;
        }
    } catch (error) {
        console.error('Fetch error:', error);
        statusMessage.textContent = `Network error: Could not connect to server. (${error.message})`;
    } finally {
        convertButton.disabled = false; // Re-enable the button
    }
});

// Optional: Clear status message when user starts typing again
textInput.addEventListener('input', () => {
    statusMessage.textContent = '';
});