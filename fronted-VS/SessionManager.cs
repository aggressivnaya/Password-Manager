using System;

namespace password_manager
{
    public class SessionManager
    {
        private static SessionManager _instance;
        private static readonly object _lock = new object();
        
        public int UserId { get; private set; }
        public string Username { get; private set; }
        public string Email { get; private set; }
        public string AuthToken { get; private set; }
        public bool IsLoggedIn => !string.IsNullOrEmpty(AuthToken);
        
        // Event to notify when login state changes
        public event EventHandler LoginStateChanged;
        
        private SessionManager() { }
        
        public static SessionManager Instance
        {
            get
            {
                if (_instance == null)
                {
                    lock (_lock)
                    {
                        if (_instance == null)
                        {
                            _instance = new SessionManager();
                        }
                    }
                }
                return _instance;
            }
        }
        
        public void SetSession(int userId, string username, string email, string authToken)
        {
            UserId = userId;
            Username = username;
            Email = email;
            AuthToken = authToken;
            
            // Notify subscribers that login state has changed
            LoginStateChanged?.Invoke(this, EventArgs.Empty);
        }
        
        public void ClearSession()
        {
            UserId = 0;
            Username = null;
            Email = null;
            AuthToken = null;
            
            // Notify subscribers that login state has changed
            LoginStateChanged?.Invoke(this, EventArgs.Empty);
        }
    }
}