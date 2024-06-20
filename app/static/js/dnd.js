// Function to send POST request
async function sendPostRequest(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        // Handle non-OK responses
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }

        // Parse and return the JSON response
        const responseData = await response.json();
        return responseData;
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        return null;
    }
}

// Function to save the status of the task
async function saveStatus(el, target, source, sibling, post_url) {
    try {
        // Extract task ID from the href attribute
        const urlParams = new URLSearchParams(el.getAttribute('href').split('?')[1]);
        const id = urlParams.get('id');

        // Define the URL and data for the POST request
        const url = post_url;
        const data = { 'task_id': id, 'new_status': target.id };

        // Send POST request and handle the response
        const response = await sendPostRequest(url, data);
        if (response) {
            console.log('Success:', response);
        } else {
            console.error('Error: No response from server.');
        }
    } catch (error) {
        console.error('Error saving task status:', error);
    }
}