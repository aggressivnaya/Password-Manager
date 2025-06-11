using Newtonsoft.Json.Linq;
using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Navigation;

namespace password_manager
{
    public partial class AddGroupPage : Page
    {
        private Token _authToken;
        public AddGroupPage(Token authToken)
        {
            InitializeComponent();
            _authToken = authToken;
        }

        private void BackButton_Click(object sender, RoutedEventArgs e)
        {
            if (NavigationService.CanGoBack)
            {
                NavigationService.GoBack();
            }
        }

        private async void AddGroup_Click(object sender, RoutedEventArgs e)
        {
            string groupName = GroupNameTextBox.Text.Trim();
            string groupDescription = GroupDescriptionTextBox.Text.Trim();

            if (string.IsNullOrEmpty(groupName))
            {
                MessageBox.Show("Group name cannot be empty.", "Error", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            // TODO: Save group to database or state
            ApiResponse response = await Common.CreateGroup(Common.baseUrl, _authToken.access_token, groupName, groupDescription);
            //MessageBox.Show($"Group '{groupName}' added successfully!", "Success", MessageBoxButton.OK, MessageBoxImage.Information);

            if (NavigationService.CanGoBack)
            {
                NavigationService.GoBack();
            }
        }
    }
}
