document.getElementById('analyze-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const urlInput = document.getElementById('url-input').value;
    const resultDiv = document.getElementById('result');

    try {
        const response = await fetch('http://localhost:5000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: urlInput })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        resultDiv.innerHTML = `
            <p>URL: ${data.url}</p>
            <p>Score: ${data.score}</p>
            <p>Status: <span class="${data.status}">${data.status}</span></p>
        `;
    } catch (error) {
        console.error('Error analyzing the URL:', error);
        resultDiv.innerHTML = '<p>There was an error analyzing the URL. Please try again.</p>';
    }
});
