document.addEventListener('DOMContentLoaded', function() {
    // Check authentication
    if (!checkAuth()) return;
    
    // Load navbar
    loadNavbar();
    
    // Initialize tabs
    initTabs();
    
    // Get group name from URL
    const urlParams = new URLSearchParams(window.location.search);
    const groupName = urlParams.get('name');
    
    if (!groupName) {
        window.location.href = 'groups.html';
        return;
    }
    
    // DOM elements
    const groupHeader = document.getElementById('group-header');
    const groupPasswordsContainer = document.getElementById('group-passwords-container');
    const groupMembersContainer = document.getElementById('group-members-container');
    const groupRequestsContainer = document.getElementById('group-requests-container');
    const requestsTab = document.getElementById('requests-tab');
    const addGroupPasswordBtn = document.getElementById('add-group-password-btn');
    const addGroupPasswordModal = document.getElementById('add-group-password-modal');
    const editGroupPasswordModal = document.getElementById('edit-group-password-modal');
    const sendRequestModal = document.getElementById('send-request-modal');
    
    // Modal elements
    const cancelAddGroupPassword = document.getElementById('cancel-add-group-password');
    const saveGroupPassword = document.getElementById('save-group-password');
    const cancelEditGroupPassword = document.getElementById('cancel-edit-group-password');
    const updateGroupPassword = document.getElementById('update-group-password');
    const cancelSendRequest = document.getElementById('cancel-send-request');
    const submitRequest = document.getElementById('submit-request');
    
    // Form elements
    const newGroupPasswordName = document.getElementById('new-group-password-name');
    const newGroupPasswordValue = document.getElementById('new-group-password-value');
    const editGroupPasswordId = document.getElementById('edit-group-password-id');
    const editGroupPasswordName = document.getElementById('edit-group-password-name');
    const editGroupPasswordValue = document.getElementById('edit-group-password-value');
    const requestCommand = document.getElementById('request-command');
    
    // State
    let groupDetails = null;
    let requests = [];
    let isAdmin = false;
    let isMember = false;
    
    // Fetch group data
    const fetchGroupData = async () => {
        groupHeader.innerHTML = `
            <div class="loading-container">
                <div class="loading-spinner"></div>
            </div>
        `;
        
        groupPasswordsContainer.innerHTML = '';
        groupMembersContainer.innerHTML = '';
        groupRequestsContainer.innerHTML = '';
        
        try {
            const response = await getGroup(groupName);
            groupDetails = response.group;
            
            //l
            isAdmin = groupDetails.users.find(u => u.username === localStorage.getItem("username"))?.isAdmin;
            //isMember = !(group.users.find(u => u.username === localStorage.getItem("username"))?.isAdmin);
            
            // Hide requests tab if not admin
            if (!isAdmin) {
                requestsTab.style.display = 'none';
            } else {
                requestsTab.style.display = 'block';
                // Fetch requests if admin
                const resp = await getGroupRequests(groupName) || [];
                
                const requestts = (resp && resp.requests) ? resp.requests : [];
                
                // Map the data to the expected format if needed
                const rrequests = requestts.map(request => ({
                    id: request.id,
                    sender_id: request.sender_id,
                    request_command: request.request_command,
                }));
                requests = [...rrequests];
                renderGroupRequests();
            }
            
            
            renderGroupHeader();
            renderGroupPasswords();
            renderGroupMembers();
            
            
            /*if (isAdmin) {
                renderGroupRequests();
            }*/
            
            // Update modal descriptions based on role
            const addPasswordDescription = document.getElementById('add-password-description');
            const editPasswordDescription = document.getElementById('edit-password-description');
            
            if (isAdmin) {
                addPasswordDescription.textContent = 'Enter the details for the new password.';
                editPasswordDescription.textContent = 'Update the password details.';
                saveGroupPassword.textContent = 'Save Password';
                updateGroupPassword.textContent = 'Update Password';
            } else {
                addPasswordDescription.textContent = 'Your request will be sent to the group admin for approval.';
                editPasswordDescription.textContent = 'Your request will be sent to the group admin for approval.';
                saveGroupPassword.textContent = 'Send Request';
                updateGroupPassword.textContent = 'Send Request';
            }
            
        } catch (error) {
            console.error('Error fetching group details:', error);
            /*groupHeader.innerHTML = `
                <div class="text-center p-8 bg-muted rounded-lg">
                    <p class="text-lg text-muted-foreground">Failed to load group details. Please try again.</p>
                </div>
            `;*/
        }
    };
    
    // Render group header
    const renderGroupHeader = () => {
        groupHeader.innerHTML = `
            <h1 class="page-title">${groupDetails.name}</h1>
            <p class="group-description">${groupDetails.description || 'No description'}</p>
            <div class="group-role">
                    Your role: ${isAdmin ? 'Admin' : 'Member'}
            </div>
            
            <div class="group-actions">
                <button id="refresh-group-btn" class="btn btn-outline">
                    <svg xmlns="http://www.w3.org/2000/svg" class="btn-icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                        <path d="M20 11a8.1 8.1 0 0 0 -15.5 -2m-.5 -4v4h4" />
                        <path d="M4 13a8.1 8.1 0 0 0 15.5 2m.5 4v-4h-4" />
                    </svg>
                    Refresh
                </button>
                
                ${!isAdmin ? `
                    <button id="send-request-btn" class="btn btn-outline">
                        <svg xmlns="http://www.w3.org/2000/svg" class="btn-icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                            <path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0" />
                            <path d="M12 8l0 4" />
                            <path d="M12 16l.01 0" />
                        </svg>
                        Send Request
                    </button>
                ` : ''}
                
                ${!isAdmin ? `
                    <button id="leave-group-btn" class="btn btn-outline text-destructive">
                        <svg xmlns="http://www.w3.org/2000/svg" class="btn-icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                            <path d="M14 8v-2a2 2 0 0 0 -2 -2h-7a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h7a2 2 0 0 0 2 -2v-2" />
                            <path d="M9 12h12l-3 -3" />
                            <path d="M18 15l3 -3" />
                        </svg>
                        Leave Group
                    </button>
                ` : ''}
                
                ${isAdmin ? `
                    <button id="delete-group-btn" class="btn btn-destructive">
                        <svg xmlns="http://www.w3.org/2000/svg" class="btn-icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                            <path d="M4 7l16 0" />
                            <path d="M10 11l0 6" />
                            <path d="M14 11l0 6" />
                            <path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12" />
                            <path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3" />
                        </svg>
                        Delete Group
                    </button>
                ` : ''}
            </div>
        `;
        
        // Add event listeners
        document.getElementById('refresh-group-btn').addEventListener('click', fetchGroupData);
        
        if (!isAdmin) {
            document.getElementById('send-request-btn').addEventListener('click', () => {
                requestCommand.value = '';
                sendRequestModal.classList.add('open');
            });
        }
        
        if (!isAdmin) {
            document.getElementById('leave-group-btn').addEventListener('click', handleLeaveGroup);
        }
        
        if (isAdmin) {
            document.getElementById('delete-group-btn').addEventListener('click', handleDeleteGroup);
        }
    };
    
    // Render group passwords
    const renderGroupPasswords = () => {
        if (!groupDetails.sharedPasswords || groupDetails.sharedPasswords.length === 0) {
            groupPasswordsContainer.innerHTML = `
                <div class="text-center p-8 bg-muted rounded-lg">
                    <p class="text-lg text-muted-foreground">No passwords found in this group.</p>
                </div>
            `;
            return;
        }
        
        groupPasswordsContainer.innerHTML = groupDetails.sharedPasswords.map(password => `
            <div class="card" data-id="${password.name}">
                <div class="card-header">
                    <h3 class="card-title">${password.name}</h3>
                </div>
                <div class="card-content">
                    <div class="password-value-container">
                        <input type="password" value="${password.password}" readonly class="password-value" data-id="${password.name}">
                        <div class="password-actions">
                            <button class="password-action-btn toggle-group-password" data-id="${password.name}">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                    <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                                    <path d="M10 12a2 2 0 1 0 4 0a2 2 0 0 0 -4 0" />
                                    <path d="M21 12c-2.4 4 -5.4 6 -9 6c-3.6 0 -6.6 -2 -9 -6c2.4 -4 5.4 -6 9 -6c3.6 0 6.6 2 9 6" />
                                </svg>
                            </button>
                            <button class="password-action-btn copy-group-password" data-password="${password.password}">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                    <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                                    <path d="M8 8m0 2a2 2 0 0 1 2 -2h8a2 2 0 0 1 2 2v8a2 2 0 0 1 -2 2h-8a2 2 0 0 1 -2 -2z" />
                                    <path d="M16 8v-2a2 2 0 0 0 -2 -2h-8a2 2 0 0 0 -2 2v8a2 2 0 0 0 2 2h2" />
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
                <div class="card-footer">
                    <button class="btn btn-outline edit-group-password" data-id="${password.name}">
                        <svg xmlns="http://www.w3.org/2000/svg" class="btn-icon" width="16" height="16" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                            <path d="M7 7h-1a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-1" />
                            <path d="M20.385 6.585a2.1 2.1 0 0 0 -2.97 -2.97l-8.415 8.385v3h3l8.385 -8.415z" />
                            <path d="M16 5l3 3" />
                        </svg>
                        Edit
                    </button>
                    <button class="btn btn-outline delete-group-password" data-id="${password.name}" data-name="${password.name}">
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
        document.querySelectorAll('.toggle-group-password').forEach(button => {
            button.addEventListener('click', toggleGroupPasswordVisibility);
        });
        
        document.querySelectorAll('.copy-group-password').forEach(button => {
            button.addEventListener('click', copyGroupPassword);
        });
        
        document.querySelectorAll('.edit-group-password').forEach(button => {
            button.addEventListener('click', openEditGroupPasswordModal);
        });
        
        document.querySelectorAll('.delete-group-password').forEach(button => {
            button.addEventListener('click', handleDeleteGroupPassword);
        });
    };
    
    // Render group members
    const renderGroupMembers = () => {
        if (!groupDetails.users || groupDetails.users.length === 0) {
            groupMembersContainer.innerHTML = `
                <div class="text-center p-8 bg-muted rounded-lg">
                    <p class="text-lg text-muted-foreground">No members found in this group.</p>
                </div>
            `;
            return;
        }
        
        groupMembersContainer.innerHTML = groupDetails.users.map(user => `
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">${user.username}</h3>
                    <p class="card-description">Role: ${user.isAdmin ? "Admin" : "Member"}</p>
                </div>
                ${isAdmin && user.isAdmin ? `
                    <div class="card-footer">
                        <button class="btn btn-destructive w-full remove-user" data-username="${user.username}">
                            <svg xmlns="http://www.w3.org/2000/svg" class="btn-icon" width="16" height="16" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                                <path d="M9 7m-4 0a4 4 0 1 0 8 0a4 4 0 1 0 -8 0" />
                                <path d="M3 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2" />
                                <path d="M19 7l-5 5" />
                                <path d="M14 7l5 5" />
                            </svg>
                            Remove User
                        </button>
                    </div>
                ` : ''}
            </div>
        `).join('');
        
        // Add event listeners
        if (isAdmin) {
            document.querySelectorAll('.remove-user').forEach(button => {
                button.addEventListener('click', handleRemoveUser);
            });
        }
    };
    
    // Render group requests
    const renderGroupRequests = () => {
        if (!requests || requests.length === 0) {
            groupRequestsContainer.innerHTML = `
                <div class="text-center p-8 bg-muted rounded-lg">
                    <p class="text-lg text-muted-foreground">No pending requests.</p>
                </div>
            `;
            return;
        }
        
        groupRequestsContainer.innerHTML = requests.map(request => `
            <div class="card">
                <div class="card-header">
                    <div class="flex justify-between">
                        <h3 class="card-title">Request from ${request.sender_id}</h3>
                        <p class="card-description">${request.sender_id}</p>
                    </div>
                </div>
                <div class="card-content">
                    <p class="text-foreground mb-4">${request.request_command}</p>
                </div>
                <div class="card-footer">
                    <button class="btn btn-outline approve-request" data-id="${request.id}">
                        <svg xmlns="http://www.w3.org/2000/svg" class="btn-icon" width="16" height="16" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                            <path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0" />
                            <path d="M9 12l2 2l4 -4" />
                        </svg>
                        Approve
                    </button>
                    <button class="btn btn-outline decline-request" data-id="${request.id}">
                        <svg xmlns="http://www.w3.org/2000/svg" class="btn-icon" width="16" height="16" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                            <path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0" />
                            <path d="M10 10l4 4m0 -4l-4 4" />
                        </svg>
                        Decline
                    </button>
                </div>
            </div>
        `).join('');
        
        // Add event listeners
        document.querySelectorAll('.approve-request').forEach(button => {
            button.addEventListener('click', handleApproveRequest);
        });
        
        document.querySelectorAll('.decline-request').forEach(button => {
            button.addEventListener('click', handleDeclineRequest);
        });
    };
    
    // Toggle password visibility
    const toggleGroupPasswordVisibility = (e) => {
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
    const copyGroupPassword = (e) => {
        const password = e.currentTarget.getAttribute('data-password');
        navigator.clipboard.writeText(password);
        showToast('Password copied to clipboard');
    };
    
    // Open edit password modal
    const openEditGroupPasswordModal = (e) => {
        const id = parseInt(e.currentTarget.getAttribute('data-id'));
        const password = groupDetails.passwords.find(p => p.id === id);
        
        if (password) {
            editGroupPasswordId.value = password.id;
            editGroupPasswordName.value = password.name;
            editGroupPasswordValue.value = password.password;
            
            editGroupPasswordModal.classList.add('open');
        }
    };
    
    // Handle delete password
    const handleDeleteGroupPassword = async (e) => {
        const id = parseInt(e.currentTarget.getAttribute('data-id'));
        const name = e.currentTarget.getAttribute('data-name');
        
        if (confirm('Are you sure you want to delete this password?')) {
            try {
                if (isAdmin) {
                    await deletePasswordFromGroup(groupName, id);
                    showToast('Password deleted successfully');
                } else {
                    await insertRequest(groupName, `del`);
                    showToast('Password delete request sent to admin');
                }
                fetchGroupData();
            } catch (error) {
                console.error('Error deleting password:', error);
                showToast('Failed to delete password');
            }
        }
    };
    
    // Handle approve request
    const handleApproveRequest = async (e) => {
        const id = parseInt(e.currentTarget.getAttribute('data-id'));
        
        try {
            await approveRequest(groupName, id);
            showToast('Request approved successfully');
            fetchGroupData();
        } catch (error) {
            console.error('Error approving request:', error);
            showToast('Failed to approve request');
        }
    };
    
    // Handle decline request
    const handleDeclineRequest = async (e) => {
        const id = parseInt(e.currentTarget.getAttribute('data-id'));
        
        try {
            await declineRequest(groupName, id);
            showToast('Request declined successfully');
            fetchGroupData();
        } catch (error) {
            console.error('Error declining request:', error);
            showToast('Failed to decline request');
        }
    };
    
    // Handle remove user
    const handleRemoveUser = async (e) => {
        const username = e.currentTarget.getAttribute('data-username');
        
        if (confirm(`Are you sure you want to remove ${username} from the group?`)) {
            try {
                await removeUser(groupName, username);
                showToast('User removed successfully');
                fetchGroupData();
            } catch (error) {
                console.error('Error removing user:', error);
                showToast('Failed to remove user');
            }
        }
    };
    
    // Handle leave group
    const handleLeaveGroup = async () => {
        if (confirm('Are you sure you want to leave this group?')) {
            try {
                await leaveGroup(groupName);
                showToast('You have left the group');
                window.location.href = 'groups.html';
            } catch (error) {
                console.error('Error leaving group:', error);
                showToast('Failed to leave group');
            }
        }
    };
    
    // Handle delete group
    const handleDeleteGroup = async () => {
        if (confirm('Are you sure you want to delete this group? This action cannot be undone.')) {
            try {
                await removeGroup(groupName);
                showToast('Group deleted successfully');
                window.location.href = 'groups.html';
            } catch (error) {
                console.error('Error deleting group:', error);
                showToast('Failed to delete group');
            }
        }
    };
    
    // Event listeners
    addGroupPasswordBtn.addEventListener('click', () => {
        newGroupPasswordName.value = '';
        newGroupPasswordValue.value = '';
        addGroupPasswordModal.classList.add('open');
    });
    
    cancelAddGroupPassword.addEventListener('click', () => {
        addGroupPasswordModal.classList.remove('open');
    });
    
    saveGroupPassword.addEventListener('click', async () => {
        if (!newGroupPasswordName.value || !newGroupPasswordValue.value) {
            showToast('Please fill in all fields');
            return;
        }
        
        try {
            if (isAdmin) {
                await addPasswordToGroup(
                    groupName,
                    newGroupPasswordValue.value,
                    newGroupPasswordName.value
                );
                showToast('Password added successfully');
            } else {
                await insertRequest(
                    groupName,
                    `add`
                );
                showToast('Password add request sent to admin');
            }
            
            addGroupPasswordModal.classList.remove('open');
            fetchGroupData();
        } catch (error) {
            console.error('Error adding password:', error);
            showToast('Failed to add password');
        }
    });
    
    cancelEditGroupPassword.addEventListener('click', () => {
        editGroupPasswordModal.classList.remove('open');
    });
    
    updateGroupPassword.addEventListener('click', async () => {
        if (!editGroupPasswordName.value || !editGroupPasswordValue.value) {
            showToast('Please fill in all fields');
            return;
        }
    
        try {
            if (isAdmin) {
                await updatePasswordInGroup(
                    groupName,
                    parseInt(editGroupPasswordId.value),
                    editGroupPasswordValue.value,
                    editGroupPasswordName.value
                );
                showToast('Password updated successfully');
            } else {
                await insertRequest(
                    groupName,
                    `upd`
                );
                showToast('Password update request sent to admin');
            }
    
            editGroupPasswordModal.classList.remove('open');
            fetchGroupData();
        } catch (error) {
            console.error('Error updating password:', error);
            showToast('Failed to update password');
        }
    });
    
    
    cancelSendRequest.addEventListener('click', () => {
        sendRequestModal.classList.remove('open');
    });
    
    submitRequest.addEventListener('click', async () => {
        if (!requestCommand.value) {
            showToast('Please enter a request');
            return;
        }
        
        try {
            await insertRequest(groupName, requestCommand.value);
            sendRequestModal.classList.remove('open');
            showToast('Request sent successfully');
        } catch (error) {
            console.error('Error sending request:', error);
            showToast('Failed to send request');
        }
    });
    
    // Close modals when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === addGroupPasswordModal) {
            addGroupPasswordModal.classList.remove('open');
        }
        if (e.target === editGroupPasswordModal) {
            editGroupPasswordModal.classList.remove('open');
        }
        if (e.target === sendRequestModal) {
            sendRequestModal.classList.remove('open');
        }
    });
    
    // Initial fetch
    fetchGroupData();
});