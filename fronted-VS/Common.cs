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
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using password_manager.Models;

namespace password_manager
{
    public class User
    {
        public string username { get; set; }
        public string email { get; set; }

        public User(string username, string email)
        {
            this.username = username;
            this.email = email;
        }
    }

    public class Common
    {
        private static readonly HttpClient _httpClient = new HttpClient();
        private readonly string _authUrl = "http://182.20.1.3:5000";
        private readonly string _dalUrl = "http://182.20.1.4:5001";

        public Common()
        {
            //_httpClient = new HttpClient();
        }

        public async Task<string> SignupAsync(User user)
        {
            var response = await _httpClient.PostAsJsonAsync($"{_authUrl}/signup/", user);
            if (response.IsSuccessStatusCode)
            {
                var result = await response.Content.ReadAsAsync<dynamic>();
                return result.access_token;
            }
            else
            {
                Console.WriteLine($"Signup failed: {response.ReasonPhrase}");
                return null;
            }
        }

        public async Task<string> LoginAsync(User user)
        {
            var response = await _httpClient.PostAsJsonAsync($"{_authUrl}/login/", user);
            if (response.IsSuccessStatusCode)
            {
                var result = await response.Content.ReadAsAsync<dynamic>();
                return result.access_token;
            }
            else
            {
                Console.WriteLine($"Login failed: {response.ReasonPhrase}");
                return null;
            }
        }

        public async Task<bool> ValidateTokenAsync(string token)
        {
            _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
            var response = await _httpClient.PostAsync($"{_authUrl}/validate/", null);
            return response.IsSuccessStatusCode;
        }

        public async Task<string> AddPasswordAsync(string token, string name, string password, bool shared)
        {
            var requestBody = new { name, password, shared };
            var content = new StringContent(System.Text.Json.JsonSerializer.Serialize(requestBody), Encoding.UTF8, "application/json");
            _httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

            var response = await _httpClient.PostAsync($"{_dalUrl}/changes/add/", content);
            return await response.Content.ReadAsStringAsync();
        }

        public async Task<string> UpdatePasswordAsync(string token, int passwordId, string newPassword, string newName, bool shared)
        {
            var requestBody = new { currPasswordId = passwordId, newPassword, newName, shared };
            var content = new StringContent(System.Text.Json.JsonSerializer.Serialize(requestBody), Encoding.UTF8, "application/json");
            _httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

            var response = await _httpClient.PostAsync($"{_dalUrl}/changes/update/", content);
            return await response.Content.ReadAsStringAsync();
        }

        public async Task<string> DeletePasswordAsync(string token, int passwordId)
        {
            var requestBody = new { currPasswordId = passwordId };
            var content = new StringContent(System.Text.Json.JsonSerializer.Serialize(requestBody), Encoding.UTF8, "application/json");
            _httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

            var response = await _httpClient.DeleteAsync($"{_dalUrl}/changes/delete/");
            return await response.Content.ReadAsStringAsync();
        }

        public async Task<List<PasswordItem>> GetUserPasswordsAsync(string token)
        {
            _httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);
            var response = await _httpClient.GetAsync($"{_dalUrl}/getPasswords");

            if (response.IsSuccessStatusCode)
            {
                var jsonString = await response.Content.ReadAsStringAsync();
                var passwords = JsonConvert.DeserializeObject<List<PasswordItem>>(jsonString);
                return passwords;
            }

            return new List<PasswordItem>();
        }

        public async Task<string> CreateGroupAsync(string token, string groupName, string description)
        {
            var requestBody = new { name = groupName, description };
            var content = new StringContent(System.Text.Json.JsonSerializer.Serialize(requestBody), Encoding.UTF8, "application/json");
            _httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

            var response = await _httpClient.PostAsync($"{_dalUrl}/group/create_group", content);
            return await response.Content.ReadAsStringAsync();
        }

        public async Task<string> JoinGroupAsync(string token, string groupLink)
        {
            var requestBody = new { groupLink };
            var content = new StringContent(System.Text.Json.JsonSerializer.Serialize(requestBody), Encoding.UTF8, "application/json");
            _httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

            var response = await _httpClient.GetAsync($"{_dalUrl}/group/enter_group");
            return await response.Content.ReadAsStringAsync();
        }

        // New methods for group functionality

        public async Task<List<GroupItem>> GetUserGroupsAsync(string token)
        {
            _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
            var response = await _httpClient.GetAsync($"{_dalUrl}/group/get_user_groups");

            if (response.IsSuccessStatusCode)
            {
                var jsonString = await response.Content.ReadAsStringAsync();
                var groups = JsonConvert.DeserializeObject<List<GroupItem>>(jsonString);
                return groups;
            }

            return new List<GroupItem>();
        }

        public async Task<List<PasswordItem>> GetGroupPasswordsAsync(string token, int groupId)
        {
            _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
            var response = await _httpClient.GetAsync($"{_dalUrl}/group/{groupId}/passwords");

            if (response.IsSuccessStatusCode)
            {
                var jsonString = await response.Content.ReadAsStringAsync();
                var passwords = JsonConvert.DeserializeObject<List<PasswordItem>>(jsonString);
                return passwords;
            }

            return new List<PasswordItem>();
        }

        public async Task<List<GroupMemberItem>> GetGroupMembersAsync(string token, int groupId)
        {
            _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
            var response = await _httpClient.GetAsync($"{_dalUrl}/group/{groupId}/members");

            if (response.IsSuccessStatusCode)
            {
                var jsonString = await response.Content.ReadAsStringAsync();
                var members = JsonConvert.DeserializeObject<List<GroupMemberItem>>(jsonString);
                return members;
            }

            return new List<GroupMemberItem>();
        }

        public async Task<bool> SendJoinRequestAsync(string token, int groupId, string message)
        {
            var requestBody = new { groupId, message };
            var content = new StringContent(JsonConvert.SerializeObject(requestBody), Encoding.UTF8, "application/json");
            _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);

            var response = await _httpClient.PostAsync($"{_dalUrl}/group/request/join", content);
            return response.IsSuccessStatusCode;
        }

        public async Task<List<GroupRequestItem>> GetPendingGroupRequestsAsync(string token, int groupId)
        {
            _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
            var response = await _httpClient.GetAsync($"{_dalUrl}/group/{groupId}/requests");

            if (response.IsSuccessStatusCode)
            {
                var jsonString = await response.Content.ReadAsStringAsync();
                var requests = JsonConvert.DeserializeObject<List<GroupRequestItem>>(jsonString);
                return requests;
            }

            return new List<GroupRequestItem>();
        }

        public async Task<bool> RespondToGroupRequestAsync(string token, int requestId, bool accept)
        {
            var requestBody = new { requestId, accept };
            var content = new StringContent(JsonConvert.SerializeObject(requestBody), Encoding.UTF8, "application/json");
            _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);

            var response = await _httpClient.PostAsync($"{_dalUrl}/group/request/respond", content);
            return response.IsSuccessStatusCode;
        }

        public async Task<bool> LeaveGroupAsync(string token, int groupId)
        {
            _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
            var response = await _httpClient.PostAsync($"{_dalUrl}/group/{groupId}/leave", null);
            return response.IsSuccessStatusCode;
        }

        public async Task<bool> RemoveUserFromGroupAsync(string token, int groupId, int userId)
        {
            var requestBody = new { userId };
            var content = new StringContent(JsonConvert.SerializeObject(requestBody), Encoding.UTF8, "application/json");
            _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);

            var response = await _httpClient.PostAsync($"{_dalUrl}/group/{groupId}/remove_user", content);
            return response.IsSuccessStatusCode;
        }

        public async Task<bool> MakeUserManagerAsync(string token, int groupId, int userId)
        {
            var requestBody = new { userId };
            var content = new StringContent(JsonConvert.SerializeObject(requestBody), Encoding.UTF8, "application/json");
            _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);

            var response = await _httpClient.PostAsync($"{_dalUrl}/group/{groupId}/make_manager", content);
            return response.IsSuccessStatusCode;
        }

        public async Task<bool> SendPasswordEditRequestAsync(string token, int groupId, int passwordId, string newPassword, string reason)
        {
            var requestBody = new { groupId, passwordId, newPassword, reason };
            var content = new StringContent(JsonConvert.SerializeObject(requestBody), Encoding.UTF8, "application/json");
            _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);

            var response = await _httpClient.PostAsync($"{_dalUrl}/group/password/edit_request", content);
            return response.IsSuccessStatusCode;
        }

        public async Task<List<PasswordEditRequestItem>> GetPasswordEditRequestsAsync(string token, int groupId)
        {
            _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
            var response = await _httpClient.GetAsync($"{_dalUrl}/group/{groupId}/password_edit_requests");

            if (response.IsSuccessStatusCode)
            {
                var jsonString = await response.Content.ReadAsStringAsync();
                var requests = JsonConvert.DeserializeObject<List<PasswordEditRequestItem>>(jsonString);
                return requests;
            }

            return new List<PasswordEditRequestItem>();
        }
    }
}