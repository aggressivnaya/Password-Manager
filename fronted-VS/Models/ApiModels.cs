using System;
using System.Collections.Generic;

namespace password_manager.Models
{
    public class GroupItem
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public bool IsManager { get; set; }
        public int MemberCount { get; set; }
        public int PasswordCount { get; set; }
        public DateTime CreatedDate { get; set; }
        
        // Helper property for UI display
        public string Icon => GetIconForGroup();
        public string Info => $"{MemberCount} members • {PasswordCount} passwords";
        
        private string GetIconForGroup()
        {
            // Simple logic to assign icons based on group name
            if (Name.ToLower().Contains("work") || Name.ToLower().Contains("team"))
                return "👥";
            else if (Name.ToLower().Contains("family"))
                return "👪";
            else if (Name.ToLower().Contains("home") || Name.ToLower().Contains("device"))
                return "🏠";
            else
                return "🔐";
        }
    }

    public class PasswordItem
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Username { get; set; }
        public string EncryptedPassword { get; set; }
        public bool IsShared { get; set; }
        public int? GroupId { get; set; }
        public string GroupName { get; set; }
        public DateTime CreatedDate { get; set; }
        public DateTime ModifiedDate { get; set; }
        
        // Helper property for UI display
        public string Icon => GetIconForPassword();
        
        private string GetIconForPassword()
        {
            string nameLower = Name.ToLower();
            
            if (nameLower.Contains("gmail") || nameLower.Contains("email") || nameLower.Contains("mail"))
                return "📧";
            else if (nameLower.Contains("work") || nameLower.Contains("office") || nameLower.Contains("company"))
                return "💼";
            else if (nameLower.Contains("bank") || nameLower.Contains("pay") || nameLower.Contains("money"))
                return "💰";
            else if (nameLower.Contains("social") || nameLower.Contains("facebook") || nameLower.Contains("twitter"))
                return "📱";
            else
                return "🌐";
        }
    }

    public class GroupMemberItem
    {
        public int Id { get; set; }
        public int UserId { get; set; }
        public string Username { get; set; }
        public string Email { get; set; }
        public bool IsManager { get; set; }
        public DateTime JoinedDate { get; set; }
        
        // Helper property for UI display
        public string Role => IsManager ? "Manager" : "Member";
        public string Icon => IsManager ? "👑" : "👤";
    }

    public enum RequestStatus
    {
        Pending,
        Approved,
        Rejected
    }

    public class GroupRequestItem
    {
        public int Id { get; set; }
        public int GroupId { get; set; }
        public string GroupName { get; set; }
        public int UserId { get; set; }
        public string Username { get; set; }
        public string Message { get; set; }
        public RequestStatus Status { get; set; }
        public DateTime RequestDate { get; set; }
        
        // Helper properties for UI display
        public bool IsPending => Status == RequestStatus.Pending;
        public string StatusText => Status.ToString();
        public string TimeAgo => GetTimeAgo(RequestDate);
        
        private string GetTimeAgo(DateTime dateTime)
        {
            TimeSpan timeSince = DateTime.Now - dateTime;
            
            if (timeSince.TotalSeconds < 60)
                return $"{(int)timeSince.TotalSeconds} seconds ago";
            if (timeSince.TotalMinutes < 60)
                return $"{(int)timeSince.TotalMinutes} minutes ago";
            if (timeSince.TotalHours < 24)
                return $"{(int)timeSince.TotalHours} hours ago";
            if (timeSince.TotalDays < 30)
                return $"{(int)timeSince.TotalDays} days ago";
            
            return dateTime.ToShortDateString();
        }
    }

    public class PasswordEditRequestItem
    {
        public int Id { get; set; }
        public int GroupId { get; set; }
        public int PasswordId { get; set; }
        public string PasswordName { get; set; }
        public int RequestedByUserId { get; set; }
        public string RequestedByUsername { get; set; }
        public string NewPassword { get; set; }
        public string Reason { get; set; }
        public RequestStatus Status { get; set; }
        public DateTime RequestDate { get; set; }
        
        // Helper properties for UI display
        public bool IsPending => Status == RequestStatus.Pending;
        public string StatusText => Status.ToString();
        public string TimeAgo => GetTimeAgo(RequestDate);
        
        private string GetTimeAgo(DateTime dateTime)
        {
            TimeSpan timeSince = DateTime.Now - dateTime;
            
            if (timeSince.TotalSeconds < 60)
                return $"{(int)timeSince.TotalSeconds} seconds ago";
            if (timeSince.TotalMinutes < 60)
                return $"{(int)timeSince.TotalMinutes} minutes ago";
            if (timeSince.TotalHours < 24)
                return $"{(int)timeSince.TotalHours} hours ago";
            if (timeSince.TotalDays < 30)
                return $"{(int)timeSince.TotalDays} days ago";
            
            return dateTime.ToShortDateString();
        }
    }
}