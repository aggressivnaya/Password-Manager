using password_manager.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace password_manager
{
    public partial class PasswordsPage : Page
    {
        private Common _apiClient;
        private int _groupId;
        private string _groupName;
        private bool _isManager;
        private List<PasswordItem> _passwords;
        private string _authToken;

        public PasswordsPage(int groupId, string groupName, bool isManager)
        {
            InitializeComponent();

            _groupId = groupId;
            _groupName = groupName;
            _isManager = isManager;

            // Get the API client
            //_apiClient = new Common();

            // Get the auth token from session manager
            //_authToken = SessionManager.Instance.AuthToken;

            // Initialize UI
            //InitializeUI();

            // Load passwords
           // LoadPasswordsAsync();
        }

        private void InitializeUI()
        {
            // Set page title
            PageName.Text = $"{_groupName} Passwords";

            // Set group info text
            //GroupInfo.Text = $"Group: {_groupName} • You are a {(_isManager ? "manager" : "member")}";
        }
        /*
        private async void LoadPasswordsAsync()
        {
            try
            {
                // Show loading indicator if you have one
                // LoadingIndicator.Visibility = Visibility.Visible;

                // Get passwords from the server
                _passwords = await _apiClient.GetGroupPasswordsAsync(_authToken, _groupId);

                // Clear existing items
                var listBox = (ListBox)FindName("PasswordsListBox");
                if (listBox != null)
                {
                    listBox.Items.Clear();

                    // Add items for each password
                    foreach (var password in _passwords)
                    {
                        // Create the grid layout for the password item
                        Grid grid = new Grid();

                        // Define columns
                        ColumnDefinition col1 = new ColumnDefinition();
                        col1.Width = GridLength.Auto;
                        ColumnDefinition col2 = new ColumnDefinition();
                        col2.Width = new GridLength(1, GridUnitType.Star);
                        ColumnDefinition col3 = new ColumnDefinition();
                        col3.Width = new GridLength(1, GridUnitType.Star);
                        ColumnDefinition col4 = new ColumnDefinition();
                        col4.Width = GridLength.Auto;

                        grid.ColumnDefinitions.Add(col1);
                        grid.ColumnDefinitions.Add(col2);
                        grid.ColumnDefinitions.Add(col3);
                        grid.ColumnDefinitions.Add(col4);

                        // Icon
                        TextBlock iconBlock = new TextBlock();
                        iconBlock.Text = password.Icon;
                        iconBlock.FontSize = 20;
                        iconBlock.Margin = new Thickness(0, 0, 15, 0);
                        Grid.SetColumn(iconBlock, 0);
                        grid.Children.Add(iconBlock);

                        // Password info
                        StackPanel infoPanel = new StackPanel();

                        TextBlock nameBlock = new TextBlock();
                        nameBlock.Text = password.Name;
                        nameBlock.FontWeight = FontWeights.Bold;
                        infoPanel.Children.Add(nameBlock);

                        TextBlock usernameBlock = new TextBlock();
                        usernameBlock.Text = password.Username;
                        usernameBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FFaaaaaa"));
                        infoPanel.Children.Add(usernameBlock);

                        Grid.SetColumn(infoPanel, 1);
                        grid.Children.Add(infoPanel);
                        
                        grid.Children.Add(infoPanel);

                        // Password display
                        StackPanel passwordPanel = new StackPanel();

                        TextBlock passwordTextBlock = new TextBlock();
                        passwordTextBlock.Name = "passwordTextBlock" + password.Id; // Unique name
                        passwordTextBlock.Text = "••••••••";
                        passwordTextBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FFaaaaaa"));
                        passwordTextBlock.FontWeight = FontWeights.Bold;
                        passwordTextBlock.FontSize = 20;
                        passwordTextBlock.HorizontalAlignment = HorizontalAlignment.Center;
                        passwordPanel.Children.Add(passwordTextBlock);

                        Grid.SetColumn(passwordPanel, 2);
                        grid.Children.Add(passwordPanel);

                        // Action buttons
                        StackPanel buttonPanel = new StackPanel();
                        buttonPanel.Orientation = Orientation.Horizontal;

                        // View button (always visible)
                        Button viewButton = new Button();
                        viewButton.Content = "👁";
                        viewButton.Margin = new Thickness(0, 0, 10, 0);
                        viewButton.Style = (Style)FindResource("ModernButton");
                        viewButton.Tag = password.Id;
                        viewButton.Click += ViewPassword_Click;
                        buttonPanel.Children.Add(viewButton);

                        // Edit button (visible only for managers)
                        Button editButton = new Button();
                        editButton.Content = "🖊️";
                        editButton.Margin = new Thickness(0, 0, 10, 0);
                        editButton.Style = (Style)FindResource("ModernButton");
                        editButton.Tag = password.Id;
                        editButton.Click += EditButton_Click;
                        editButton.Visibility = _isManager ? Visibility.Visible : Visibility.Collapsed;
                        buttonPanel.Children.Add(editButton);

                        // Request Edit button (visible only for members)
                        Button requestEditButton = new Button();
                        requestEditButton.Content = "📝";
                        requestEditButton.Margin = new Thickness(0, 0, 10, 0);
                        requestEditButton.Style = (Style)FindResource("RequestEditButton");
                        requestEditButton.Tag = password.Id;
                        requestEditButton.Click += RequestEditButton_Click;
                        requestEditButton.Visibility = _isManager ? Visibility.Collapsed : Visibility.Visible;
                        requestEditButton.ToolTip = "Request Edit";
                        buttonPanel.Children.Add(requestEditButton);

                        // Delete button (visible only for managers)
                        Button deleteButton = new Button();
                        deleteButton.Content = "🗑️";
                        deleteButton.Style = (Style)FindResource("IconButton");
                        deleteButton.Tag = password.Id;
                        deleteButton.Click += DeletePassword_Click;
                        deleteButton.Visibility = _isManager ? Visibility.Visible : Visibility.Collapsed;
                        buttonPanel.Children.Add(deleteButton);

                        Grid.SetColumn(buttonPanel, 3);
                        grid.Children.Add(buttonPanel);

                        // Add the grid to a list box item
                        ListBoxItem item = new ListBoxItem();
                        item.Content = grid;
                        item.Style = (Style)FindResource("PasswordListBoxItem");

                        // Add to the list box
                        listBox.Items.Add(item);
                    }
                }

                // Check if there are pending password edit requests if user is a manager
                if (_isManager)
                {
                    var editRequests = await _apiClient.GetPasswordEditRequestsAsync(_authToken, _groupId);
                    RequestsButton.Visibility = editRequests.Count > 0 ? Visibility.Visible : Visibility.Collapsed;
                }
                else
                {
                    RequestsButton.Visibility = Visibility.Collapsed;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading passwords: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
            finally
            {
                // Hide loading indicator if you have one
                // LoadingIndicator.Visibility = Visibility.Collapsed;
            }
        }*/

        private void EditButton_Click(object sender, RoutedEventArgs e)
        {
            if (NavigationService != null && NavigationService.CanGoBack)
            {
                NavigationService.GoBack();
            }
        }

        private void BackButton_Click(object sender, RoutedEventArgs e)
        {
            if (NavigationService != null && NavigationService.CanGoBack)
            {
                NavigationService.GoBack();
            }
        }

        private async void ViewPassword_Click(object sender, RoutedEventArgs e)
        {
            // Get the button that was clicked
            Button button = sender as Button;
            if (button != null && button.Tag != null)
            {
                int passwordId = Convert.ToInt32(button.Tag);

                // Find the password
                PasswordItem selectedPassword = null;
                foreach (var password in _passwords)
                {
                    if (password.Id == passwordId)
                    {
                        selectedPassword = password;
                        break;
                    }
                }

                if (selectedPassword != null)
                {
                    // Find the password TextBlock
                    TextBlock passwordBlock = (TextBlock)FindName("passwordTextBlock" + passwordId);

                    if (passwordBlock != null)
                    {
                        // Toggle password visibility
                        if (passwordBlock.Text == "••••••••")
                        {
                            // Decrypt the password (in a real app, you'd use your encryption helper)
                            passwordBlock.Text = selectedPassword.EncryptedPassword; // This would be decrypted
                            button.Content = "🔒";
                        }
                        else
                        {
                            passwordBlock.Text = "••••••••";
                            button.Content = "👁";
                        }
                    }
                }
            }
        }
        /*
        private void EditButton_Click(object sender, RoutedEventArgs e)
        {
            // Only managers can edit directly
            if (!_isManager)
            {
                MessageBox.Show("Only group managers can edit passwords directly.",
                    "Access Denied", MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }

            // Get the button that was clicked
            Button button = sender as Button;
            if (button != null && button.Tag != null)
            {
                int passwordId = Convert.ToInt32(button.Tag);

                // Find the password
                PasswordItem selectedPassword = null;
                foreach (var password in _passwords)
                {
                    if (password.Id == passwordId)
                    {
                        selectedPassword = password;
                        break;
                    }
                }

                if (selectedPassword != null)
                {
                    // TODO: Navigate to password edit page
                    // For now, just show a message
                    MessageBox.Show($"Editing password for {selectedPassword.Name}.",
                        "Edit Password", MessageBoxButton.OK, MessageBoxImage.Information);
                }
            }
        }*/

        private void RequestEditButton_Click(object sender, RoutedEventArgs e)
        {
            // Get the button that was clicked
            Button button = sender as Button;
            if (button != null && button.Tag != null)
            {
                int passwordId = Convert.ToInt32(button.Tag);

                // Find the password
                PasswordItem selectedPassword = null;
                foreach (var password in _passwords)
                {
                    if (password.Id == passwordId)
                    {
                        selectedPassword = password;
                        break;
                    }
                }

                if (selectedPassword != null)
                {
                    // Navigate to request edit dialog
                    NavigationService?.Navigate(new RequestEditPasswordDialog());//_groupId, passwordId, selectedPassword.Name
                }
            }
        }

        private void SettingsButton_Click(object sender, RoutedEventArgs e)
        {
            // Navigate to group settings page
            NavigationService?.Navigate(new GroupSettingsPage());//_groupId, _groupName, _isManager
        }

        private void RequestsButton_Click(object sender, RoutedEventArgs e)
        {
            // Only managers can view requests
            if (_isManager)
            {
                // Navigate to group requests page
                NavigationService?.Navigate(new GroupRequestsPage(_groupId));
            }
            else
            {
                MessageBox.Show("Only group managers can view and manage requests.",
                    "Access Denied", MessageBoxButton.OK, MessageBoxImage.Information);
            }
        }

        private async void DeletePassword_Click(object sender, RoutedEventArgs e)
        {
            // Only managers can delete
            if (!_isManager)
            {
                MessageBox.Show("Only group managers can delete passwords.",
                    "Access Denied", MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }

            // Get the button that was clicked
            Button button = sender as Button;
            if (button != null && button.Tag != null)
            {
                int passwordId = Convert.ToInt32(button.Tag);

                // Find the password
                PasswordItem selectedPassword = null;
                foreach (var password in _passwords)
                {
                    if (password.Id == passwordId)
                    {
                        selectedPassword = password;
                        break;
                    }
                }

                if (selectedPassword != null)
                {
                    // Confirm deletion
                    MessageBoxResult result = MessageBox.Show($"Are you sure you want to delete the password for {selectedPassword.Name}?",
                        "Confirm Deletion", MessageBoxButton.YesNo, MessageBoxImage.Warning);

                    if (result == MessageBoxResult.Yes)
                    {
                        try
                        {
                            // Delete the password
                            string response = await _apiClient.DeletePasswordAsync(_authToken, passwordId);

                            // Reload passwords
                            //LoadPasswordsAsync();
                        }
                        catch (Exception ex)
                        {
                            MessageBox.Show($"Error deleting password: {ex.Message}",
                                "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                        }
                    }
                }
            }
        }

        private void AddNewPassword_Click(object sender, RoutedEventArgs e)
        {
            // Check if user has permission to add password
            if (!_isManager)
            {
                MessageBox.Show("Only group managers can add new passwords to the group.",
                    "Permission Denied", MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }

            // TODO: Navigate to add password page
            // For now, just show a message
            MessageBox.Show("Adding new password to group.",
                "Add Password", MessageBoxButton.OK, MessageBoxImage.Information);
        }
    }
}
