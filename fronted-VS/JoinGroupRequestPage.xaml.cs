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
        
        private Token _authToken;
        public JoinGroupRequestPage(Token token)
        {
            _authToken = token;
            InitializeComponent();
        }

        private void BackButton_Click(object sender, RoutedEventArgs e)
        {
            // Navigate back to the groups page
            NavigationService?.GoBack();
        }

        private async void SendJoinRequest_Click(object sender, RoutedEventArgs e)
        {
            // Validate input
            if (string.IsNullOrWhiteSpace(GroupNameTextBox.Text))
            {
                MessageBox.Show("Please enter a group name.", "Input Required", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            try
            {
                
                ApiResponse res = await Common.EnterGroup(Common.baseUrl,_authToken.access_token , GroupNameTextBox.Text.ToString());
                if (res.Success != 200)
                {
                    MessageBox.Show("Error sending join request",
                    "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                    return;
                }
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