document.addEventListener('DOMContentLoaded', function() {
    // Check authentication
    if (!checkAuth()) return;
    
    // Load navbar
    loadNavbar();
    
    // DOM elements
    const groupsContainer = document.getElementById('groups-container');
    const searchInput = document.getElementById('search-groups');
    const refreshBtn = document.getElementById('refresh-btn');
    const createGroupBtn = document.getElementById('create-group-btn');
    const joinGroupBtn = document.getElementById('join-group-btn');
    const createGroupModal = document.getElementById('create-group-modal');
    const joinGroupModal = document.getElementById('join-group-modal');
    
    // Modal elements
    const cancelCreateGroup = document.getElementById('cancel-create-group');
    const saveGroup = document.getElementById('save-group');
    const cancelJoinGroup = document.getElementById('cancel-join-group');
    const sendJoinRequest = document.getElementById('send-join-request');
    
    // Form elements
    const newGroupName = document.getElementById('new-group-name');
    const newGroupDescription = document.getElementById('new-group-description');
    const joinGroupName = document.getElementById('join-group-name');
    
    // State
    let groups = [];
    let filteredGroups = [];
    
    // Fetch groups
    const fetchGroups = async () => {
        groupsContainer.innerHTML = `
            <div class="loading-container">
                <div class="loading-spinner"></div>
            </div>
        `;
        
        try {
            const response = await getGroups() || [];
            groups = (response && response.groups) ? response.groups : [];
        
            // Map the data to the expected format if needed
            groups = groups.map( name => ({ name }));

            filteredGroups = [...groups];
            renderGroups();
        } catch (error) {
            console.error('Error fetching groups:', error);
            groupsContainer.innerHTML = `
                <div class="text-center p-8 bg-muted rounded-lg">
                    <p class="text-lg text-muted-foreground">Failed to load groups. Please try again.</p>
                </div>
            `;
        }
    };
    
    // Render groups
    const renderGroups = () => {
        if (filteredGroups.length === 0) {
            groupsContainer.innerHTML = `
                <div class="text-center p-8 bg-muted rounded-lg">
                    <p class="text-lg text-muted-foreground">
                        ${searchInput.value ? 'No groups match your search' : 'No groups found. Create your first group!'}
                    </p>
                </div>
            `;
            return;
        }
        
        groupsContainer.innerHTML = filteredGroups.map(group => `
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">${group.name}</h3>
                    ${group.created_at ? `<p class="card-description">Created: ${new Date(group.created_at).toLocaleDateString()}</p>` : ''}
                </div>
                <div class="card-content">
                    <p class="text-muted-foreground mb-4">${group.description || 'No description'}</p>
                    <div class="flex items-center justify-between">
                        <div class="flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" class="icon mr-2" width="20" height="20" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                                <path d="M9 7m-4 0a4 4 0 1 0 8 0a4 4 0 1 0 -8 0" />
                                <path d="M3 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2" />
                                <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                                <path d="M21 21v-2a4 4 0 0 0 -3 -3.85" />
                            </svg>
                            <span class="text-sm text-muted-foreground">${group.member_count || 0} members</span>
                        </div>
                        ${group.role ? `
                            <span class="badge badge-purple">${group.role}</span>
                        ` : ''}
                    </div>
                </div>
                <div class="card-footer">
                    <button class="btn btn-primary btn-gradient-green w-full view-group" data-name="${group.name}">
                        View Group
                        <svg xmlns="http://www.w3.org/2000/svg" class="ml-2" width="16" height="16" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                            <path d="M5 12l14 0" />
                            <path d="M13 18l6 -6" />
                            <path d="M13 6l6 6" />
                        </svg>
                    </button>
                </div>
            </div>
        `).join('');
        
        // Add event listeners
        document.querySelectorAll('.view-group').forEach(button => {
            button.addEventListener('click', navigateToGroup);
        });
    };
    
    // Navigate to group
    const navigateToGroup = (e) => {
        const groupName = e.currentTarget.getAttribute('data-name');
        window.location.href = `group-details.html?name=${encodeURIComponent(groupName)}`;
    };
    
    // Filter groups
    const handleSearch = (e) => {
        const searchTerm = e.target.value.toLowerCase();
        filteredGroups = filterItems(groups, searchTerm, (group, term) => 
            group.name.toLowerCase().includes(term) || 
            (group.description && group.description.toLowerCase().includes(term))
        );
        renderGroups();
    };
    
    // Event listeners
    searchInput.addEventListener('input', handleSearch);
    
    refreshBtn.addEventListener('click', fetchGroups);
    
    createGroupBtn.addEventListener('click', () => {
        newGroupName.value = '';
        newGroupDescription.value = '';
        createGroupModal.classList.add('open');
    });
    
    joinGroupBtn.addEventListener('click', () => {
        joinGroupName.value = '';
        joinGroupModal.classList.add('open');
    });
    
    cancelCreateGroup.addEventListener('click', () => {
        createGroupModal.classList.remove('open');
    });
    
    saveGroup.addEventListener('click', async () => {
        if (!newGroupName.value) {
            showToast('Please enter a group name');
            return;
        }
        
        try {
            await createGroup(newGroupName.value, newGroupDescription.value);
            createGroupModal.classList.remove('open');
            showToast('Group created successfully');
            fetchGroups();
        } catch (error) {
            console.error('Error creating group:', error);
            showToast('Failed to create group');
        }
    });
    
    cancelJoinGroup.addEventListener('click', () => {
        joinGroupModal.classList.remove('open');
    });
    
    sendJoinRequest.addEventListener('click', async () => {
        if (!joinGroupName.value) {
            showToast('Please enter a group name');
            return;
        }
        
        try {
            await enterGroup(joinGroupName.value);
            joinGroupModal.classList.remove('open');
            showToast('Join request sent successfully');
            fetchGroups();
        } catch (error) {
            console.error('Error joining group:', error);
            showToast('Failed to join group');
        }
    });
    
    // Close modals when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === createGroupModal) {
            createGroupModal.classList.remove('open');
        }
        if (e.target === joinGroupModal) {
            joinGroupModal.classList.remove('open');
        }
    });
    
    // Initial fetch
    fetchGroups();
});