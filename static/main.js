document.getElementById('search-form').addEventListener('submit', function (event) {
    event.preventDefault();
    
    let query = document.getElementById('query').value;
    let resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'query': query
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        displayResults(data);
        displayChart(data);  // Call the function to display the chart
    });
});

function displayResults(data) {
    let resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<h2>Results</h2>';
    for (let i = 0; i < data.documents.length; i++) {
        let docDiv = document.createElement('div');
        docDiv.innerHTML = `<strong>Document ${data.indices[i]}</strong><p>${data.documents[i]}</p><br><strong>Similarity: ${data.similarities[i]}</strong>`;
        resultsDiv.appendChild(docDiv);
    }
}

function displayChart(data) {
    // Extract the necessary data for the chart
    const documentLabels = data.documents.map((_, i) => `Doc ${i + 1}`);  // Create labels like Doc 1, Doc 2, ...
    const similarities = data.similarities;  // Cosine similarity values
    
    // Define the chart data and layout using Plotly
    const trace = {
        x: documentLabels,  // X-axis labels (Document 1, Document 2, etc.)
        y: similarities,    // Y-axis values (Cosine similarity scores)
        type: 'bar'         // Bar chart type
    };

    const layout = {
        title: 'Cosine Similarities of Top 5 Documents',
        xaxis: {
            title: 'Documents'
        },
        yaxis: {
            title: 'Cosine Similarity'
        }
    };

    // Render the chart in the 'similarity-chart' div
    Plotly.newPlot('similarity-chart', [trace], layout);
}
