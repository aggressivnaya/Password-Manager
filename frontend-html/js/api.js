// API functions to interact with the backend

// Base URL for API requests
//const API_BASE_URL = "http://182.20.1.2:5002";
const API_BASE_URL = "http://127.0.0.1:5002";

// Store token in localStorage
const setToken = (token) => {
    localStorage.setItem("token", token);
};

// Get token from localStorage
const getToken = () => {
    return localStorage.getItem("token");
};

// Clear token from localStorage
const clearToken = () => {
    localStorage.removeItem("token");
};

// Check if user is authenticated
const isAuthenticated = () => {
    return !!getToken();
};

// API request helper function
const apiRequest = async (endpoint, method = "GET", data = null) => {
    const token = getToken();
    const headers = {
        "Content-Type": "application/json",
    };

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const options = {
        method,
        headers,
    };

    if (data && (method === "POST" || method === "PUT")) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "API request failed");
        }

        return await response.json();
    } catch (error) {
        console.error("API request error:", error);
        throw error;
    }
};

// Auth API functions
const login = async (username, email) => {
    localStorage.setItem("username", username);
    localStorage.setItem("email", email);
    const response = await apiRequest("/login", "POST", { username, email });
    if (response.access_token) {
        setToken(response.access_token);
    }
    return response;
};

const signup = async (username, email) => {
    localStorage.setItem("username", username);
    localStorage.setItem("email", email);
    const response = await apiRequest("/signup", "POST", { username, email });
    if (response.access_token) {
        setToken(response.access_token);
    }
    return response;
};

const logout = async () => {
    const response = await apiRequest("/logout", "DELETE");
    clearToken();
    return response;
};

// User API functions
const getUserInfo = async () => {
    return await apiRequest("/user");
};

// Password API functions
const getPasswords = async () => {
    return await apiRequest("/passwords", "GET");
};

const addPassword = async (password, name, shared = "False") => {
    const queryParams = new URLSearchParams({ password, name, shared }).toString();
    return await apiRequest(`/passwords/add?${queryParams}`, "POST");
};

const updatePassword = async (currPasswordId, newPassword, newName, shared = "False") => {
    const queryParams = new URLSearchParams({
        currPasswordId: currPasswordId,
        newPassword,
        newName,
        shared,
    }).toString();
    return await apiRequest(`/passwords/update?${queryParams}`, "POST");
};

const deletePassword = async (currPasswordId) => {
    const queryParams = new URLSearchParams({ currPasswordId: currPasswordId.toString() }).toString();
    return await apiRequest(`/passwords/delete?${queryParams}`, "DELETE");
};

// Group API functions
const getGroups = async () => {
    return await apiRequest("/groups");
};

const getGroup = async (groupName) => {
    const queryParams = new URLSearchParams({ groupName: groupName }).toString();
    return await apiRequest(`/groups/${groupName}?${queryParams}`);
};

const createGroup = async (groupName, description) => {
    const queryParams = new URLSearchParams({ description }).toString();
    return await apiRequest(`/groups/${groupName}/createGroup?${queryParams}`, "POST");
};

const enterGroup = async (groupName) => {
    return await apiRequest(`/groups/${groupName}/enterGroup`, "POST");
};

const leaveGroup = async (groupName) => {
    return await apiRequest(`/groups/${groupName}/leaveGroup`, "DELETE");
};

const removeGroup = async (groupName) => {
    return await apiRequest(`/groups/${groupName}/removeGroup`, "DELETE");
};

const addPasswordToGroup = async (groupName, password, name, shared = "true") => {
    const queryParams = new URLSearchParams({ password, name, shared }).toString();
    return await apiRequest(`/groups/${groupName}/passwords/add?${queryParams}`, "POST");
};

const updatePasswordInGroup = async (groupName, passwordId, newPassword, newName, shared = "true") => {
    const queryParams = new URLSearchParams({
        passwordId: passwordId.toString(),
        newPassword,
        newName,
        shared,
    }).toString();
    return await apiRequest(`/groups/${groupName}/passwords/update?${queryParams}`, "POST");
};

const deletePasswordFromGroup = async (groupName, passwordId) => {
    const queryParams = new URLSearchParams({ passwordId: passwordId.toString() }).toString();
    return await apiRequest(`/groups/${groupName}/passwords/delete?${queryParams}`, "DELETE");
};

const getGroupRequests = async (groupName) => {
    return await apiRequest(`/groups/${groupName}/requests`);
};

const insertRequest = async (groupName, command) => {
    const queryParams = new URLSearchParams({ command }).toString();
    return await apiRequest(`/groups/${groupName}/insertRequest?${queryParams}`, "POST");
};

const approveRequest = async (groupName, requestId) => {
    const queryParams = new URLSearchParams({ requestId: requestId.toString() }).toString();
    return await apiRequest(`/groups/${groupName}/approveRequest?${queryParams}`, "POST");
};

const declineRequest = async (groupName, requestId) => {
    const queryParams = new URLSearchParams({ requestId: requestId.toString() }).toString();
    return await apiRequest(`/groups/${groupName}/declineRequest?${queryParams}`, "DELETE");
};

const acceptUser = async (groupName, username) => {
    const queryParams = new URLSearchParams({ username }).toString();
    return await apiRequest(`/groups/${groupName}/acceptUser?${queryParams}`, "POST");
};

const removeUser = async (groupName, user) => {
    const queryParams = new URLSearchParams({ user }).toString();
    return await apiRequest(`/groups/${groupName}/removeUser?${queryParams}`, "DELETE");
};

// History API functions
const getHistory = async () => {
    return await apiRequest("/history");
};