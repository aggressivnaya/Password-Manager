document.addEventListener('DOMContentLoaded', function() {
    // Check authentication
    if (!checkAuth()) return;
    
    // Load navbar
    loadNavbar();
    
    // DOM elements
    const passwordsContainer = document.getElementById('passwords-container');
    const searchInput = document.getElementById('search-passwords');
    const refreshBtn = document.getElementById('refresh-btn');
    const addPasswordBtn = document.getElementById('add-password-btn');
    const addPasswordModal = document.getElementById('add-password-modal');
    const editPasswordModal = document.getElementById('edit-password-modal');
    
    // Modal elements
    const cancelAddPassword = document.getElementById('cancel-add-password');
    const savePassword = document.getElementById('save-password');
    const cancelEditPassword = document.getElementById('cancel-edit-password');
    const updatePasswordBtn = document.getElementById('update-password');
    
    // Form elements
    const newPasswordName = document.getElementById('new-password-name');
    const newPasswordValue = document.getElementById('new-password-value');
    const newPasswordShared = document.getElementById('new-password-shared');
    const editPasswordId = document.getElementById('edit-password-id');
    const editPasswordName = document.getElementById('edit-password-name');
    const editPasswordValue = document.getElementById('edit-password-value');
    const editPasswordShared = document.getElementById('edit-password-shared');
    
    // State
    let passwords = [];
    let filteredPasswords = [];
    
    // Fetch passwords
    const fetchPasswords = async () => {
        passwordsContainer.innerHTML = `
            <div class="loading-container">
                <div class="loading-spinner"></div>
            </div>
        `;
        
        try {
            // Get the response from the API
        const response = await getPasswords();
        
        // Extract the passwords array from the response
        // If response has a 'passwords' key, use that, otherwise use empty array
        passwords = (response && response.passwords) ? response.passwords : [];
        
        // Map the data to the expected format if needed
        passwords = passwords.map(p => ({
            id: p.id,
            name: p.name,
            // Use 'value' property as 'password' if that's how backend returns it
            password: p.value,
            shared: p.shared,
            created_at: p.created_at
        }));
        
        filteredPasswords = [...passwords];
        renderPasswords();
        } catch (error) {
            console.error('Error fetching passwords:', error);
            passwordsContainer.innerHTML = `
                <div class="text-center p-8 bg-muted rounded-lg">
                    <p class="text-lg text-muted-foreground">Failed to load passwords. Please try again.</p>
                </div>
            `;
        }
    };
    
    // Render passwords
    const renderPasswords = () => {
        if (filteredPasswords.length === 0) {
            passwordsContainer.innerHTML = `
                <div class="text-center p-8 bg-muted rounded-lg">
                    <p class="text-lg text-muted-foreground">
                        ${searchInput.value ? 'No passwords match your search' : 'No passwords found. Add your first password!'}
                    </p>
                </div>
            `;
            return;
        }
        
        passwordsContainer.innerHTML = filteredPasswords.map(password => `
            <div class="card" data-id="${password.id}">
                <div class="card-header">
                    <h3 class="card-title">${password.name}</h3>
                    ${password.created_at ? `<p class="card-description">Created: ${new Date(password.created_at).toLocaleDateString()}</p>` : ''}
                </div>
                <div class="card-content">
                    <div class="password-value-container">
                        <input type="password" value="${password.password}" readonly class="password-value" data-id="${password.id}">
                        <div class="password-actions">
                            <button class="password-action-btn toggle-password" data-id="${password.id}">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                    <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                                    <path d="M10 12a2 2 0 1 0 4 0a2 2 0 0 0 -4 0" />
                                    <path d="M21 12c-2.4 4 -5.4 6 -9 6c-3.6 0 -6.6 -2 -9 -6c2.4 -4 5.4 -6 9 -6c3.6 0 6.6 2 9 6" />
                                </svg>
                            </button>
                            <button class="password-action-btn copy-password" data-password="${password.password}">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                    <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                                    <path d="M8 8m0 2a2 2 0 0 1 2 -2h8a2 2 0 0 1 2 2v8a2 2 0 0 1 -2 2h-8a2 2 0 0 1 -2 -2z" />
                                    <path d="M16 8v-2a2 2 0 0 0 -2 -2h-8a2 2 0 0 0 -2 2v8a2 2 0 0 0 2 2h2" />
                                </svg>
                            </button>
                        </div>
                    </div>
                    ${password.shared ? `
                        <div class="mt-2">
                            <span class="badge badge-green">Shared</span>
                        </div>
                    ` : ''}
                </div>
                <div class="card-footer">
                    <button class="btn btn-outline edit-password" data-id="${password.id}">
                        <svg xmlns="http://www.w3.org/2000/svg" class="btn-icon" width="16" height="16" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                            <path d="M7 7h-1a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-1" />
                            <path d="M20.385 6.585a2.1 2.1 0 0 0 -2.97 -2.97l-8.415 8.385v3h3l8.385 -8.415z" />
                            <path d="M16 5l3 3" />
                        </svg>
                        Edit
                    </button>
                    <button class="btn btn-outline delete-password" data-id="${password.id}">
                        <svg xmlns="http://www.w3.org/2000/svg" class="btn-icon" width="16" height="16" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                            <path d="M4 7l16 0" />
                            <path d="M10 11l0 6" />
                            <path d="M14 11l0 6" />
                            <path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12" />
                            <path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3" />
                        </svg>
                        Delete
                    </button>
                </div>
            </div>
        `).join('');
        
        // Add event listeners
        document.querySelectorAll('.toggle-password').forEach(button => {
            button.addEventListener('click', togglePasswordVisibility);
        });
        
        document.querySelectorAll('.copy-password').forEach(button => {
            button.addEventListener('click', copyPassword);
        });
        
        document.querySelectorAll('.edit-password').forEach(button => {
            button.addEventListener('click', openEditPasswordModal);
        });
        
        document.querySelectorAll('.delete-password').forEach(button => {
            button.addEventListener('click', handleDeletePassword);
        });
    };
    
    // Toggle password visibility
    const togglePasswordVisibility = (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        const input = document.querySelector(`.password-value[data-id="${id}"]`);
        
        if (input.type === 'password') {
            input.type = 'text';
            e.currentTarget.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                    <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                    <path d="M3 3l18 18" />
                    <path d="M10.584 10.587a2 2 0 0 0 2.828 2.83" />
                    <path d="M9.363 5.365a9.466 9.466 0 0 1 2.637 -.365c3.6 0 6.6 2 9 6c-.817 1.361 -1.723 2.462 -2.715 3.304m-2.285 1.696c-1.237 .507 -2.588 .761 -4 .761c-3.6 0 -6.6 -2 -9 -6c2.4 -4 5.4 -6 9 -6c3.6 0 6.6 2 9 6" />
                </svg>
            `;
        } else {
            input.type = 'password';
            e.currentTarget.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                    <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                    <path d="M10 12a2 2 0 1 0 4 0a2 2 0 0 0 -4 0" />
                    <path d="M21 12c-2.4 4 -5.4 6 -9 6c-3.6 0 -6.6 -2 -9 -6c2.4 -4 5.4 -6 9 -6c3.6 0 6.6 2 9 6" />
                </svg>
            `;
        }
    };
    
    // Copy password to clipboard
    const copyPassword = (e) => {
        const password = e.currentTarget.getAttribute('data-password');
        navigator.clipboard.writeText(password);
        showToast('Password copied to clipboard');
    };
    
    // Open edit password modal
    const openEditPasswordModal = (e) => {
        const id = parseInt(e.currentTarget.getAttribute('data-id'));
        const password = passwords.find(p => p.id === id);
        
        if (password) {
            editPasswordId.value = password.id;
            editPasswordName.value = password.name;
            editPasswordValue.value = password.password;
            editPasswordShared.checked = password.shared;
            
            editPasswordModal.classList.add('open');
        }
    };
    
    // Handle delete password
    const handleDeletePassword = async (e) => {
        const id = parseInt(e.currentTarget.getAttribute('data-id'));
        
        if (confirm('Are you sure you want to delete this password?')) {
            try {
                await deletePassword(id);
                showToast('Password deleted successfully');
                fetchPasswords();
            } catch (error) {
                console.error('Error deleting password:', error);
                showToast('Failed to delete password', 'error');
            }
        }
    };
    
    // Filter passwords
    const handleSearch = (e) => {
        const searchTerm = e.target.value.toLowerCase();
        filteredPasswords = filterItems(passwords, searchTerm, (password, term) => 
            password.name.toLowerCase().includes(term)
        );
        renderPasswords();
    };
    
    // Event listeners
    searchInput.addEventListener('input', handleSearch);
    
    refreshBtn.addEventListener('click', fetchPasswords);
    
    addPasswordBtn.addEventListener('click', () => {
        newPasswordName.value = '';
        newPasswordValue.value = '';
        newPasswordShared.checked = false;
        addPasswordModal.classList.add('open');
    });
    
    cancelAddPassword.addEventListener('click', () => {
        addPasswordModal.classList.remove('open');
    });
    
    savePassword.addEventListener('click', async () => {
        if (!newPasswordName.value || !newPasswordValue.value) {
            showToast('Please fill in all fields');
            return;
        }
        
        try {
            await addPassword(
                newPasswordValue.value,
                newPasswordName.value,
                newPasswordShared.checked ? 'True' : 'False'
            );
            addPasswordModal.classList.remove('open');
            showToast('Password added successfully');
            fetchPasswords();
        } catch (error) {
            console.error('Error adding password:', error);
            showToast('Failed to add password');
        }
    });
    
    cancelEditPassword.addEventListener('click', () => {
        editPasswordModal.classList.remove('open');
    });
    
    updatePasswordBtn.addEventListener('click', async () => {
        if (!editPasswordName.value || !editPasswordValue.value) {
            showToast('Please fill in all fields');
            return;
        }
        
        try {
            await updatePassword(
                parseInt(editPasswordId.value),
                editPasswordValue.value,
                editPasswordName.value,
                editPasswordShared.checked ? 'True' : 'False'
            );
            editPasswordModal.classList.remove('open');
            showToast('Password updated successfully');
            fetchPasswords();
        } catch (error) {
            console.error('Error updating password:', error);
            showToast('Failed to update password');
        }
    });
    
    // Close modals when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === addPasswordModal) {
            addPasswordModal.classList.remove('open');
        }
        if (e.target === editPasswordModal) {
            editPasswordModal.classList.remove('open');
        }
    });
    
    // Initial fetch
    fetchPasswords();
});