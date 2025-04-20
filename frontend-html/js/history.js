document.addEventListener('DOMContentLoaded', function() {
    // Check authentication
    if (!checkAuth()) return;
    
    // Load navbar
    loadNavbar();
    
    // DOM elements
    const historyContainer = document.getElementById('history-container');
    const searchInput = document.getElementById('search-history');
    const refreshBtn = document.getElementById('refresh-btn');
    
    // State
    let historyItems = [];
    let filteredItems = [];
    
    // Fetch history
    const fetchHistory = async () => {
        historyContainer.innerHTML = `
            <div class="loading-container">
                <div class="loading-spinner"></div>
            </div>
        `;
        
        try {
            const response = await getHistory();

            historyItems = (response && response.history) ? response.history : [];
            historyItems = historyItems.map(item => ({
                id: item.id,
                name: item.name,
                password: item.password,
                method: item.method,
                date: item.date,
            }));
            filteredItems = [...historyItems];
            renderHistory();
        } catch (error) {
            console.error('Error fetching history:', error);
            historyContainer.innerHTML = `
                <div class="text-center p-8 bg-muted rounded-lg">
                    <p class="text-lg text-muted-foreground">Failed to load history. Please try again.</p>
                </div>
            `;
        }
    };
    
    // Render history
    const renderHistory = () => {
        if (filteredItems.length === 0) {
            historyContainer.innerHTML = `
                <div class="text-center p-8 bg-muted rounded-lg">
                    <p class="text-lg text-muted-foreground">
                        ${searchInput.value ? 'No history items match your search' : 'No history found.'}
                    </p>
                </div>
            `;
            return;
        }
        
        historyContainer.innerHTML = filteredItems.map(item => `
            <div class="card">
                <div class="card-header">
                    <div class="flex justify-between items-center">
                        <h3 class="card-title flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" class="icon mr-2" width="20" height="20" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                                <path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0" />
                                <path d="M12 12l3 2" />
                                <path d="M12 7v5" />
                            </svg>
                            ${item.method}
                        </h3>
                        <p class="card-description">${formatDate(item.date)}</p>
                    </div>
                </div>
                <div class="card-content">
                        <p class="text-muted-foreground">${item.name}: ${item.password}</p>
                </div>
            </div>
        `).join('');
    };
    
    // Filter history
    const handleSearch = (e) => {
        const searchTerm = e.target.value.toLowerCase();
        filteredItems = filterItems(historyItems, searchTerm, (item, term) => 
            item.method.toLowerCase().includes(term) || 
            (item.method && item.method.toLowerCase().includes(term))
        );
        renderHistory();
    };
    
    // Event listeners
    searchInput.addEventListener('input', handleSearch);
    
    refreshBtn.addEventListener('click', fetchHistory);
    
    // Initial fetch
    fetchHistory();
});