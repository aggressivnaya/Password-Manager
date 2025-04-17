// API functions to interact with the backend

// Base URL for API requests
const API_BASE_URL = "http://182.20.1.2:5002"

// Store token in localStorage
const setToken = (token: string) => {
  localStorage.setItem("token", token)
}

// Get token from localStorage
const getToken = (): string | null => {
  if (typeof window !== "undefined") {
    return localStorage.getItem("token")
  }
  return null
}

// Clear token from localStorage
const clearToken = () => {
  localStorage.removeItem("token")
}

// Check if user is authenticated
export const isAuthenticated = (): boolean => {
  return !!getToken()
}

// API request helper function
const apiRequest = async (endpoint: string, method = "GET", data: any = null) => {
  const token = getToken()
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  }

  if (token) {
    headers["Authorization"] = `Bearer ${token}`
  }

  const options: RequestInit = {
    method,
    headers,
  }

  if (data && (method === "POST" || method === "PUT")) {
    options.body = JSON.stringify(data)
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, options)

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || "API request failed")
    }

    return await response.json()
  } catch (error) {
    console.error("API request error:", error)
    throw error
  }
}

// Auth API functions
export const login = async (username: string, email: string) => {
  const response = await apiRequest("/login", "POST", { username, email })
  if (response.access_token) {
    setToken(response.access_token)
  }
  return response
}

export const signup = async (username: string, email: string) => {
  const response = await apiRequest("/signup", "POST", { username, email })
  if (response.access_token) {
    setToken(response.access_token)
  }
  return response
}

export const logout = async () => {
  const response = await apiRequest("/logout")
  clearToken()
  return response
}

// User API functions
export const getUserInfo = async () => {
  return await apiRequest("/user")
}

// Password API functions
export const getPasswords = async () => {
  return await apiRequest("/passwords")
}

export const addPassword = async (password: string, name: string, shared = "false") => {
  const queryParams = new URLSearchParams({ password, name, shared }).toString()
  return await apiRequest(`/passwords/add?${queryParams}`, "POST")
}

export const updatePassword = async (
  currPasswordId: number,
  newPassword: string,
  newName: string,
  shared = "false",
) => {
  const queryParams = new URLSearchParams({
    currPasswordId: currPasswordId.toString(),
    newPassword,
    newName,
    shared,
  }).toString()
  return await apiRequest(`/passwords/update?${queryParams}`, "POST")
}

export const deletePassword = async (currPasswordId: number) => {
  const queryParams = new URLSearchParams({ currPasswordId: currPasswordId.toString() }).toString()
  return await apiRequest(`/passwords/delete?${queryParams}`, "DELETE")
}

// Group API functions
export const getGroups = async () => {
  return await apiRequest("/groups")
}

export const getGroup = async (groupName: string) => {
  return await apiRequest(`/groups/${groupName}`)
}

export const createGroup = async (groupName: string, description: string) => {
  const queryParams = new URLSearchParams({ description }).toString()
  return await apiRequest(`/groups/${groupName}/createGroup?${queryParams}`, "POST")
}

export const enterGroup = async (groupName: string) => {
  return await apiRequest(`/groups/${groupName}/enterGroup`, "POST")
}

export const leaveGroup = async (groupName: string) => {
  return await apiRequest(`/groups/${groupName}/leaveGroup`, "DELETE")
}

export const removeGroup = async (groupName: string) => {
  return await apiRequest(`/groups/${groupName}/removeGroup`, "DELETE")
}

export const addPasswordToGroup = async (groupName: string, password: string, name: string, shared = "true") => {
  const queryParams = new URLSearchParams({ password, name, shared }).toString()
  return await apiRequest(`/groups/${groupName}/passwords/add?${queryParams}`, "POST")
}

export const updatePasswordInGroup = async (
  groupName: string,
  passwordId: number,
  newPassword: string,
  newName: string,
  shared = "true",
) => {
  const queryParams = new URLSearchParams({
    passwordId: passwordId.toString(),
    newPassword,
    newName,
    shared,
  }).toString()
  return await apiRequest(`/groups/${groupName}/passwords/update?${queryParams}`, "POST")
}

export const deletePasswordFromGroup = async (groupName: string, passwordId: number) => {
  const queryParams = new URLSearchParams({ passwordId: passwordId.toString() }).toString()
  return await apiRequest(`/groups/${groupName}/passwords/delete?${queryParams}`, "DELETE")
}

export const getGroupRequests = async (groupName: string) => {
  return await apiRequest(`/groups/${groupName}/requests`)
}

export const insertRequest = async (groupName: string, command: string) => {
  const queryParams = new URLSearchParams({ command }).toString()
  return await apiRequest(`/groups/${groupName}/insertRequest?${queryParams}`, "POST")
}

export const approveRequest = async (groupName: string, requestId: number) => {
  const queryParams = new URLSearchParams({ requestId: requestId.toString() }).toString()
  return await apiRequest(`/groups/${groupName}/approveRequest?${queryParams}`, "POST")
}

export const declineRequest = async (groupName: string, requestId: number) => {
  const queryParams = new URLSearchParams({ requestId: requestId.toString() }).toString()
  return await apiRequest(`/groups/${groupName}/declineRequest?${queryParams}`, "DELETE")
}

export const acceptUser = async (groupName: string, username: string) => {
  const queryParams = new URLSearchParams({ username }).toString()
  return await apiRequest(`/groups/${groupName}/acceptUser?${queryParams}`, "POST")
}

export const removeUser = async (groupName: string, user: string) => {
  const queryParams = new URLSearchParams({ user }).toString()
  return await apiRequest(`/groups/${groupName}/removeUser?${queryParams}`, "DELETE")
}

// History API functions
export const getHistory = async () => {
  return await apiRequest("/history")
}
