using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace password_manager
{
    public class PasswordManager
    {
        private Dictionary<string, string> users = new Dictionary<string, string>();
        private Dictionary<string, List<Password>> privatePasswords = new Dictionary<string, List<Password>>();
        private List<Group> groups = new List<Group>();
        public string CurrentUser { get; private set; }

        public PasswordManager()
        {
            // Sample data for demonstration
            users["user@example.com"] = "password123"; // In practice, use hashed passwords
            privatePasswords["user@example.com"] = new List<Password>
            {
                new Password { Website = "example.com", Username = "user123", PasswordText = "password1" },
                new Password { Website = "testsite.com", Username = "user456", PasswordText = "password2" }
            };

            groups.Add(new Group
            {
                GroupName = "Family",
                Members = new List<string> { "user@example.com" },
                GroupPasswords = new List<Password>
                {
                    new Password { Website = "sharedsite.com", Username = "sharedUser", PasswordText = "sharedpass1" }
                }
            });
        }

        public bool Login(string email, string password)
        {
            if (users.ContainsKey(email) && users[email] == password)
            {
                CurrentUser = email;
                return true;
            }
            return false;
        }

        public void Logout()
        {
            CurrentUser = null;
        }

        public List<Password> GetPrivatePasswords()
        {
            return privatePasswords.ContainsKey(CurrentUser) ? privatePasswords[CurrentUser] : new List<Password>();
        }

        public List<Group> GetGroups()
        {
            return groups.Where(g => g.Members.Contains(CurrentUser)).ToList();
        }

        public List<Password> GetGroupPasswords(string groupName)
        {
            return groups.FirstOrDefault(g => g.GroupName == groupName)?.GroupPasswords ?? new List<Password>();
        }
    }
}
