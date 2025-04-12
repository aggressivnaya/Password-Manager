using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Net.Http.Formatting;
using Newtonsoft.Json.Linq;
using System.Linq.Expressions;

namespace password_manager
{
    // Response Models
    public class Token
    {
        public string access_token { get; set; }
        public string token_type { get; set; }
    }

    public class Password
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Value { get; set; }
        public bool Shared { get; set; }
    }

    public class PasswordListResponse
    {
        public List<Password> Passwords { get; set; }
    }


    public class GroupListResponse
    {
        public List<string> Groups { get; set; }
    }

    public class GroupResponse
    {
        public string Name { get; set; }
        public string Description { get; set; }
        public List<UserGroup> Users { get; set; }
        public List<SharedPassword> SharedPasswords { get; set; }
    }

    public class User
    {
        public int Id { get; set; }
        public string Username { get; set; }
        public string Email { get; set; }
    }

    public class UserGroup
    {
        public int Id { get; set; }
        public string Username { get; set; }
        public string Email { get; set; }
        public bool IsAdmin {  get; set; }
    }

    public class SharedPassword
    {
        public string Name { get; set; }
        public string Password { get; set; }
    }

    public class HistoryItem
    {
        public int Id { get; set; }
        public string Action { get; set; }
        public DateTime Timestamp { get; set; }
        public int PasswordId { get; set; }
    }

    public class HistoryResponse
    {
        public List<HistoryItem> History { get; set; }
    }

    public class Requestt
    {
        public int Id { get; set; }
        public int Sender_id { get; set; }
        public int Group_id { get; set; }
        public string Request_command { get; set; }
    }

    public class Requestts
    {
        public List<Requestt> Requests { get; set; }
    }

    public class ApiResponse
    {
        public int? Success { get; set; }
        public string Error { get; set; }
    }

    public class Common
    {
        public static string baseUrl = "http://127.0.0.1:5002";
        public Common() { }

        // Helper function to create HTTP client
        public static HttpClient CreateHttpClient(string baseUrl, string token)
        {
            var client = new HttpClient
            {
                BaseAddress = new Uri(baseUrl)
            };

            if (!string.IsNullOrEmpty(token))
            {
                client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
            }

            return client;
        }

        // Authentication Functions

        // Login to the system
        public static async Task<Token> Login(string baseUrl, string username, string email)
        {
            var client = CreateHttpClient(baseUrl, null);

            var userData = new { username = username, email = email };
            var content = new StringContent(
                JsonSerializer.Serialize(userData),
                Encoding.UTF8,
                "application/json");
            //Console.WriteLine(baseUrl+"/login");
            var response = await client.PostAsync(baseUrl + "/login", content);
            var responseContent = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseContent);
            if (response.IsSuccessStatusCode)
            {
                return JsonSerializer.Deserialize<Token>(responseContent);
            }

            throw new HttpRequestException($"Login failed: {response.StatusCode}, {responseContent}");
        }

        // Sign up for a new account
        public static async Task<Token> Signup(string baseUrl, string username, string email)
        {
            var client = CreateHttpClient(baseUrl, null);

            var userData = new { username = username, email = email };
            var content = new StringContent(
                JsonSerializer.Serialize(userData),
                Encoding.UTF8,
                "application/json");

            var response = await client.PostAsync(baseUrl + "/signup", content);
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                return JsonSerializer.Deserialize<Token>(responseContent);
            }

            throw new HttpRequestException($"Signup failed: {response.StatusCode}, {responseContent}");
        }

        // Check verification code
        public static async Task<bool> CheckVerificationCode(string baseUrl, string token, string code)
        {
            var client = CreateHttpClient(baseUrl, token);
            var response = await client.GetAsync(baseUrl + $"/check?code={Uri.EscapeDataString(code)}");
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                return bool.Parse(responseContent);
            }

            throw new HttpRequestException($"Code verification failed: {response.StatusCode}, {responseContent}");
        }

        public static async Task<User> GetUser(string baseUrl, string token)
        {
            var client = CreateHttpClient(baseUrl, token);
            var response = await client.GetAsync(baseUrl + "/user");
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                var user = JsonSerializer.Deserialize<User>(responseContent, options);
                return user;
            }

            throw new HttpRequestException($"Failed to get passwords: {response.StatusCode}, {responseContent}");
        }


        // Password Management Functions

        // Get all passwords for the current user
        public static async Task<PasswordListResponse> GetPasswords(string baseUrl, string token)
        {
            var client = CreateHttpClient(baseUrl, token);
            var response = await client.GetAsync(baseUrl + "/passwords");
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                var passwords = JsonSerializer.Deserialize<PasswordListResponse>(responseContent, options);
                return passwords;
            }

            throw new HttpRequestException($"Failed to get passwords: {response.StatusCode}, {responseContent}");
        }

        // Add a new password
        public static async Task<ApiResponse> AddPassword(string baseUrl, string token, string password, string name, bool shared)
        {
            var client = CreateHttpClient(baseUrl, token);
            var queryParams = $"password={Uri.EscapeDataString(password)}&name={Uri.EscapeDataString(name)}&shared={shared}";
            var response = await client.PostAsync($"/passwords/add?{queryParams}", null);
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                return JsonSerializer.Deserialize<ApiResponse>(responseContent);
            }

            throw new HttpRequestException($"Failed to add password: {response.StatusCode}, {responseContent}");
        }

        // Update an existing password
        public static async Task<ApiResponse> UpdatePassword(string baseUrl, string token, int passwordId, string newPassword, string newName, bool shared)
        {
            var client = CreateHttpClient(baseUrl, token);
            var queryParams = $"currPasswordId={passwordId}&newPassword={Uri.EscapeDataString(newPassword)}&newName={Uri.EscapeDataString(newName)}&shared={shared}";
            var response = await client.PostAsync(baseUrl + $"/passwords/update?{queryParams}", null);
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                return JsonSerializer.Deserialize<ApiResponse>(responseContent);
            }

            throw new HttpRequestException($"Failed to update password: {response.StatusCode}, {responseContent}");
        }

        // Delete a password
        public static async Task<ApiResponse> DeletePassword(string baseUrl, string token, int passwordId)
        {
            var client = CreateHttpClient(baseUrl, token);
            var queryParams = $"currPasswordId={passwordId}";
            var response = await client.DeleteAsync(baseUrl + $"/passwords/delete?{queryParams}");
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                return JsonSerializer.Deserialize<ApiResponse>(responseContent);
            }

            throw new HttpRequestException($"Failed to delete password: {response.StatusCode}, {responseContent}");
        }

        // Group Management Functions

        // Get all groups for the current user
        public static async Task<GroupListResponse> GetGroups(string baseUrl, string token)
        {
            var client = CreateHttpClient(baseUrl, token);
            var response = await client.GetAsync(baseUrl + "/groups");
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                return JsonSerializer.Deserialize<GroupListResponse>(responseContent, options);
            }

            throw new HttpRequestException($"Failed to get groups: {response.StatusCode}, {responseContent}");
        }

        // Get information about a specific group
        public static async Task<GroupResponse> GetGroup(string baseUrl, string token, string groupName)
        {
            var client = CreateHttpClient(baseUrl, token);
            var response = await client.GetAsync(baseUrl + $"/groups/{Uri.EscapeDataString(groupName)}");
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                var jsonDoc = JsonDocument.Parse(responseContent);
                var groupInfoJson = jsonDoc.RootElement.GetProperty("group").GetRawText();
                //var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                return JsonSerializer.Deserialize<GroupResponse>(groupInfoJson, options);
            }

            throw new HttpRequestException($"Failed to get group info: {response.StatusCode}, {responseContent}");
        }

        public static async Task<Requestts> GetGroupRequests(string baseUrl, string token, string groupName) {
            var client = CreateHttpClient(baseUrl, token);
            var response = await client.GetAsync(baseUrl + $"/groups/{Uri.EscapeDataString(groupName)}/requests?groupName={groupName}");
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {

                /*if (response.IsSuccessStatusCode)
                {
                    var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                    var passwords = JsonSerializer.Deserialize<PasswordListResponse>(responseContent, options);
                    return passwords;
                }*/
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                var jsonDoc = JsonDocument.Parse(responseContent);
                var groupInfoJson = jsonDoc.RootElement.GetProperty("requests").GetRawText();
                if(groupInfoJson == "[]")
                {
                    return null;
                }
                //JsonSerializer.Deserialize<GroupRequestsResponse>(responseContent, options);
                return JsonSerializer.Deserialize<Requestts>(responseContent, options);
            }

            throw new HttpRequestException($"Failed to get group info: {response.StatusCode}, {responseContent}");
        }

        // Add a password to a group
        public static async Task<ApiResponse> AddPasswordToGroup(string baseUrl, string token, string groupName, string password, string name, bool shared)
        {
            var client = CreateHttpClient(baseUrl, token);
            var queryParams = $"'password':{Uri.EscapeDataString(password)},'name':{Uri.EscapeDataString(name)},'shared':{shared}";
            var command = "add{" + queryParams + "}";
            var response = await client.PostAsync(baseUrl + $"/groups/{Uri.EscapeDataString(groupName)}/insertRequest?groupName={groupName}&command={command}", null);
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                return JsonSerializer.Deserialize<ApiResponse>(responseContent, options);
            }

            throw new HttpRequestException($"Failed to add password to group: {response.StatusCode}, {responseContent}");
        }

        // Delete a password from a group
        public static async Task<ApiResponse> DeletePasswordFromGroup(string baseUrl, string token, string groupName, int passwordId)
        {
            var client = CreateHttpClient(baseUrl, token);
            var queryParams = $"'passwordId':{passwordId}";
            var command = "del{" + queryParams + "}";
            var response = await client.DeleteAsync(baseUrl + $"/groups/{Uri.EscapeDataString(groupName)}/insertRequest?groupName={groupName}&command={command}");
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                return JsonSerializer.Deserialize<ApiResponse>(responseContent, options);
            }

            throw new HttpRequestException($"Failed to delete password from group: {response.StatusCode}, {responseContent}");
        }

        // Update a password in a group
        public static async Task<ApiResponse> UpdatePasswordInGroup(string baseUrl, string token, string groupName, int passwordId, string newPassword, string newName, bool shared)
        {
            var client = CreateHttpClient(baseUrl, token);
            var queryParams = $"'passwordId':{passwordId},'newPassword':{Uri.EscapeDataString(newPassword)},'name':{Uri.EscapeDataString(newName)},'shared':{shared}";
            var command = "upd{" + queryParams + "}";
            var response = await client.PostAsync(baseUrl + $"/groups/{Uri.EscapeDataString(groupName)}/insertRequest?groupName={groupName}&command={command}", null);
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                return JsonSerializer.Deserialize<ApiResponse>(responseContent, options);
            }

            throw new HttpRequestException($"Failed to update password in group: {response.StatusCode}, {responseContent}");
        }

        // Create a new group
        public static async Task<ApiResponse> CreateGroup(string baseUrl, string token, string groupName, string description)
        {
            var client = CreateHttpClient(baseUrl, token);
            var queryParams = $"description={Uri.EscapeDataString(description)}";
            var response = await client.PostAsync(baseUrl + $"/groups/{Uri.EscapeDataString(groupName)}/createGroup?{queryParams}", null);
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                return JsonSerializer.Deserialize<ApiResponse>(responseContent, options);
            }

            throw new HttpRequestException($"Failed to create group: {response.StatusCode}, {responseContent}");
        }

        // Request to join a group
        public static async Task<ApiResponse> EnterGroup(string baseUrl, string token, string groupName)
        {
            var client = CreateHttpClient(baseUrl, token);
            var command = "ent{}";
            var response = await client.PostAsync(baseUrl + $"/groups/{Uri.EscapeDataString(groupName)}/insertRequest?groupName={groupName}&command={command}", null);
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                return JsonSerializer.Deserialize<ApiResponse>(responseContent, options);
            }

            throw new HttpRequestException($"Failed to request joining group: {response.StatusCode}, {responseContent}");
        }

        // Accept a user's request to join a group
        public static async Task<ApiResponse> AcceptRequest(string baseUrl, string token, string groupName, int requestId)
        {
            var client = CreateHttpClient(baseUrl, token);
            var response = await client.PostAsync(baseUrl + $"/groups/{Uri.EscapeDataString(groupName)}/approveRequest?groupName={groupName}&requestId={requestId}", null);
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                return JsonSerializer.Deserialize<ApiResponse>(responseContent, options);
            }

            throw new HttpRequestException($"Failed to accept user: {response.StatusCode}, {responseContent}");
        }

        public static async Task<ApiResponse> DeclineRequest(string baseUrl, string token, string groupName, int requestId)
        {
            var client = CreateHttpClient(baseUrl, token);
            var response = await client.DeleteAsync(baseUrl + $"/groups/{Uri.EscapeDataString(groupName)}/declineRequest?groupName={groupName}&requestId={requestId}");
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                return JsonSerializer.Deserialize<ApiResponse>(responseContent, options);
            }

            throw new HttpRequestException($"Failed to accept user: {response.StatusCode}, {responseContent}");
        }

        // Remove a user from a group
        public static async Task<ApiResponse> RemoveUser(string baseUrl, string token, string groupName, string username)
        {
            var client = CreateHttpClient(baseUrl, token);
            var queryParams = $"user={Uri.EscapeDataString(username)}";
            var response = await client.DeleteAsync(baseUrl + $"/groups/{Uri.EscapeDataString(groupName)}/removeUser?{queryParams}");
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                return JsonSerializer.Deserialize<ApiResponse>(responseContent, options);
            }

            throw new HttpRequestException($"Failed to remove user: {response.StatusCode}, {responseContent}");
        }

        // Leave a group
        public static async Task<ApiResponse> LeaveGroup(string baseUrl, string token, string groupName)
        {
            var client = CreateHttpClient(baseUrl, token);
            var response = await client.DeleteAsync(baseUrl + $"/groups/{Uri.EscapeDataString(groupName)}/leaveGroup");
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                return JsonSerializer.Deserialize<ApiResponse>(responseContent, options);
            }

            throw new HttpRequestException($"Failed to leave group: {response.StatusCode}, {responseContent}");
        }

        // Delete a group
        public static async Task<ApiResponse> RemoveGroup(string baseUrl, string token, string groupName)
        {
            var client = CreateHttpClient(baseUrl, token);
            var response = await client.DeleteAsync(baseUrl + $"/groups/{Uri.EscapeDataString(groupName)}/removeGroup");
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                return JsonSerializer.Deserialize<ApiResponse>(responseContent, options);
            }

            throw new HttpRequestException($"Failed to remove group: {response.StatusCode}, {responseContent}");
        }

        // History Functions

        // Get password history
        public static async Task<HistoryResponse> GetHistory(string baseUrl, string token)
        {
            var client = CreateHttpClient(baseUrl, token);
            var response = await client.GetAsync(baseUrl + "/history");
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                return JsonSerializer.Deserialize<HistoryResponse>(responseContent, options);
            }

            throw new HttpRequestException($"Failed to get history: {response.StatusCode}, {responseContent}");
        }

        // Logout
        public static async Task<ApiResponse> Logout(string baseUrl, string token)
        {
            var client = CreateHttpClient(baseUrl, token);
            var response = await client.GetAsync(baseUrl + "/logout");
            var responseContent = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                return JsonSerializer.Deserialize<ApiResponse>(responseContent, options);
            }

            throw new HttpRequestException($"Failed to logout: {response.StatusCode}, {responseContent}");
        }
    }
}