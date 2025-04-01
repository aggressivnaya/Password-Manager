using System;
using System.Windows;
using System.Windows.Controls;

namespace password_manager
{
    /// <summary>
    /// Interaction logic for JoinGroupRequestPage.xaml
    /// </summary>
    public partial class JoinGroupRequestPage : Page
    {
        public JoinGroupRequestPage()
        {
            InitializeComponent();
        }

        private void BackButton_Click(object sender, RoutedEventArgs e)
        {
            // Navigate back to the groups page
            NavigationService?.GoBack();
        }

        private void SendJoinRequest_Click(object sender, RoutedEventArgs e)
        {
            // Validate input
            if (string.IsNullOrWhiteSpace(GroupNameTextBox.Text))
            {
                MessageBox.Show("Please enter a group name.", "Input Required", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            try
            {
                // TODO: Implement actual database logic to send join request
                // This would include:
                // 1. Check if group exists
                // 2. Check if user is already a member or has a pending request
                // 3. Create a new request record

                // For now, just show a success message
                MessageBox.Show($"Join request for group '{GroupNameTextBox.Text}' has been sent successfully.", 
                    "Request Sent", MessageBoxButton.OK, MessageBoxImage.Information);

                // Clear the form
                GroupNameTextBox.Text = string.Empty;
                MessageTextBox.Text = string.Empty;

                // Navigate back
                NavigationService?.GoBack();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error sending join request: {ex.Message}", 
                    "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
    }
}