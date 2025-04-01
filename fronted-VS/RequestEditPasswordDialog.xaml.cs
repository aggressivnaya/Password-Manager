using System;
using System.Windows;
using System.Windows.Controls;

namespace password_manager
{
    /// <summary>
    /// Interaction logic for RequestEditPasswordDialog.xaml
    /// </summary>
    public partial class RequestEditPasswordDialog : Page
    {
        private string _passwordName;
        private string _groupName;

        public RequestEditPasswordDialog()
        {
            InitializeComponent();
            _passwordName = "Password";
            _groupName = "Group";
        }

        

        public RequestEditPasswordDialog(string passwordName, string groupName)
        {
            InitializeComponent();
            _passwordName = passwordName;
            _groupName = groupName;
            
            // Set the password name in the form
            PasswordNameTextBox.Text = passwordName;
        }

        private void CloseButton_Click(object sender, RoutedEventArgs e)
        {
            // Navigate back
            NavigationService?.GoBack();
        }

        private void SubmitEditRequest_Click(object sender, RoutedEventArgs e)
        {
            // Validate input
            if (string.IsNullOrWhiteSpace(UsernameTextBox.Text))
            {
                MessageBox.Show("Please enter a username or email.", "Input Required", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }
            
            if (string.IsNullOrWhiteSpace(PasswordBox.Password))
            {
                MessageBox.Show("Please enter a password.", "Input Required", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }
            
            if (string.IsNullOrWhiteSpace(ReasonTextBox.Text))
            {
                MessageBox.Show("Please provide a reason for the change.", "Input Required", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            try
            {
                // TODO: Implement actual database logic to submit edit request
                // This would include:
                // 1. Create a new edit request record
                // 2. Associate it with the password and group

                // For now, just show a success message
                MessageBox.Show($"Edit request for {_passwordName} has been submitted successfully. A group manager will review your request.", 
                    "Request Submitted", MessageBoxButton.OK, MessageBoxImage.Information);

                // Navigate back
                NavigationService?.GoBack();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error submitting edit request: {ex.Message}", 
                    "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
    }
}