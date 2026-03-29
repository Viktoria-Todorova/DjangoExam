document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('book-search-input');
    const resultsContainer = document.getElementById('search-results-container');

    if (!searchInput || !resultsContainer) return;

    searchInput.addEventListener('input', function() {
        const query = this.value;
        
        if (query.length < 2) {
            return;
        }

        fetch(`/api/search/?search=${query}`)
            .then(response => response.json())
            .then(data => {
                let html = '<h1 class="results-heading">Instant Results</h1>';
                html += '<div class="results-container">';
                
                if (data.length === 0) {
                    html += '<p style="color: white; text-align: center; width: 100%;">No books found in the scrolls...</p>';
                } else {
                    data.forEach(book => {
                        // We use /rent/validate/ as base as seen in circulation/urls.py
                        html += `
                            <div class="box-details">
                                <h3>${book.title}</h3>
                                <p>Author: ${book.writer}</p>
                                ${book.quantity > 0 
                                    ? `<a href="/rent/validate/${book.id}/"><button type="button">Rent</button></a>`
                                    : '<p class="unavailable">Currently not available</p>'
                                }
                            </div>
                        `;
                    });
                }
                
                html += '</div>';
                resultsContainer.innerHTML = html;
            });
    });
});
