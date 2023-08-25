<script>
    const predictButton = document.getElementById('predict-button');
    const trainButton = document.getElementById('train-button');
    const loadingBar = document.querySelector('.loading-bar');

    predictButton.addEventListener('click', () => {
        // Code to trigger prediction and update the page
        // Use AJAX to send a request to the server
        // Update the page content with the prediction results
    });

    trainButton.addEventListener('click', () => {
        // Code to trigger training and update the page
        loadingBar.style.display = 'block';
        // Use AJAX to send a request to the server
        fetch('/train', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'stock=' + encodeURIComponent('{{ stock }}')
        })
        .then(response => response.text())
        .then(message => {
            alert(message);  // Display a message indicating success or error
            loadingBar.style.display = 'none';
        })
        .catch(error => {
            console.error('Error during training:', error);
            loadingBar.style.display = 'none';
        });
    });
</script>
