using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Navigation;

namespace password_manager
{
    public partial class AddPasswordPage : Page
    {
        private Token _authToken;
        private string _group;
        private string _command;
        //private int _passwordId;
        private Password _pass;
        public AddPasswordPage(Token token, string groupName, string command,Password password)
        {
            _authToken = token;
            _group = groupName;
            _command = command;
            //_passwordId = passwordId;
            _pass = password;
            if (_pass != null)
            {
                Shared.Text = (_pass.Shared) ? "true" : "false";
                Name.Text = _pass.Name;
                PasswordBox.Text = _pass.Value;
            }
            InitializeComponent();
        }

        private void BackButton_Click(object sender, RoutedEventArgs e)
        {
            if (NavigationService.CanGoBack)
            {
                NavigationService.GoBack();
            }
        }

        private async void SavePassword_Click(object sender, RoutedEventArgs e)
        {
            string shared = Shared.Text.Trim();
            string name = Name.Text.Trim();
            string password = PasswordBox.Text.Trim();

            if (string.IsNullOrEmpty(shared) || string.IsNullOrEmpty(name) || string.IsNullOrEmpty(password))
            {
                MessageBox.Show("All fields must be filled.", "Error", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }
            bool i = (shared == "true") ? true : false;
            ApiResponse success = new ApiResponse();
            // TODO: Save password to database or state
            if (_command == "add")
            {
                if (_group == "")
                    success = await Common.AddPassword(Common.baseUrl, _authToken.access_token, password, name, i);
                else
                    success = await Common.AddPasswordToGroup(Common.baseUrl, _authToken.access_token, _group, password, name, i);
            }
            else
            {
                if (_group == "")
                    success = await Common.UpdatePassword(Common.baseUrl, _authToken.access_token, _pass.Id, password, name, i);
                else
                    success = await Common.UpdatePasswordInGroup(Common.baseUrl, _authToken.access_token, _group, _pass.Id, password, name, i);
            }
            
            if (success.Success == 200)
            MessageBox.Show($"Password for '{name}' saved successfully!", "Success", MessageBoxButton.OK, MessageBoxImage.Information);

            if (NavigationService.CanGoBack)
            {
                NavigationService.GoBack();
            }
        }
    }
}
