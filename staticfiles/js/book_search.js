document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('book-search-input');
    const resultsContainer = document.getElementById('search-results-container');

    if (!searchInput || !resultsContainer) return;

    function fetchResults(url) {
        fetch(url)
            .then(response => response.json())
            .then(data => {
                let html = '<h1 class="results-heading" style="text-align: center; width: 100%; color: #ffd700; margin-bottom: 1.5rem;">Instant Results</h1>';
                html += '<div class="results-container">';
                
                // DRF Paginated response has 'results', 'next', 'previous'
                const books = data.results || [];
                
                if (books.length === 0) {
                    html += '<p style="color: white; text-align: center; width: 100%;">No books found in the scrolls...</p>';
                } else {
                    books.forEach(book => {
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

                // Add Pagination if needed
                if (data.next || data.previous) {
                    html += '<div class="pagination" style="margin-top: 2rem;">';
                    if (data.previous) {
                        html += `<a href="#" class="api-pagination-btn" data-url="${data.previous}">« Previous</a>`;
                    }
                    html += `<span style="padding: 10px 22px;">Page of results</span>`;
                    if (data.next) {
                        html += `<a href="#" class="api-pagination-btn" data-url="${data.next}">Next »</a>`;
                    }
                    html += '</div>';
                }

                resultsContainer.innerHTML = html;

                // Add event listeners to new pagination buttons
                document.querySelectorAll('.api-pagination-btn').forEach(btn => {
                    btn.addEventListener('click', function(e) {
                        e.preventDefault();
                        fetchResults(this.getAttribute('data-url'));
                    });
                });
            });
    }

    searchInput.addEventListener('input', function() {
        const query = this.value;
        
        if (query.length < 2) {
            // resultsContainer.innerHTML = ''; // Optional: clear if too short
            return;
        }

        fetchResults(`/api/search/?search=${query}`);
    });
});
