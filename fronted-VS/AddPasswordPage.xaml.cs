using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Navigation;

namespace password_manager
{
    public partial class AddPasswordPage : Page
    {
        public AddPasswordPage()
        {
            InitializeComponent();
        }

        private void BackButton_Click(object sender, RoutedEventArgs e)
        {
            if (NavigationService.CanGoBack)
            {
                NavigationService.GoBack();
            }
        }

        private void SavePassword_Click(object sender, RoutedEventArgs e)
        {
            string website = WebsiteTextBox.Text.Trim();
            string username = UsernameTextBox.Text.Trim();
            string password = PasswordBox.Text.Trim();

            if (string.IsNullOrEmpty(website) || string.IsNullOrEmpty(username) || string.IsNullOrEmpty(password))
            {
                MessageBox.Show("All fields must be filled.", "Error", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            // TODO: Save password to database or state
            MessageBox.Show($"Password for '{website}' saved successfully!", "Success", MessageBoxButton.OK, MessageBoxImage.Information);

            if (NavigationService.CanGoBack)
            {
                NavigationService.GoBack();
            }
        }
    }
}
