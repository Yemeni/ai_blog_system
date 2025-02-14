function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function generatePost() {
    const prompt = document.getElementById('prompt').value;
    const aiProvider = document.getElementById('ai_provider').value;

    fetch(postCreateUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            prompt: prompt,
            ai_provider: aiProvider,
            generate_only: true
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.title && data.content) {
                document.getElementById('title').value = data.title;
                document.getElementById('content').value = data.content;
            } else {
                alert("AI response missing title or content. Please try again.");
            }
        })
        .catch(error => console.error('Error:', error));
}

document.getElementById('postForm').addEventListener('submit', function (event) {
    event.preventDefault();  // Prevent default form submission

    const formData = new FormData(this);  // Collect all form fields, including CSRF token

    fetch(postCreateUrl, {
        method: 'POST',
        body: formData  // Send form-encoded data
    })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;  // Redirect to the post list if successful
            } else {
                return response.json();
            }
        })
        .then(data => {
            if (data && data.error) {
                alert("Error: " + data.error);
            }
        })
        .catch(error => console.error('Error:', error));
});
