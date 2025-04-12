
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
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
        private GroupResponse _group;
        private string _groupName;
        private bool _isManager;
        private PasswordListResponse _passwords;
        private Token _authToken;
        private string _currUser;
        //private Dictionary<int, TextBlock> _passwordTextBlocks = new Dictionary<int, TextBlock>();
        //private Dictionary<int, bool> _passwordVisibility = new Dictionary<int, bool>();

        public PasswordsPage(Token token, string groupName, bool isManager, string username)
        {
            InitializeComponent();
           
            _groupName = groupName;
            _isManager = isManager;
            _passwords = new PasswordListResponse();
            _authToken = token;
            _currUser = username;
           
            // Initialize UI
            InitializeUI();

            // Load passwords
            LoadPasswordsAsync();
        }

        private async void InitializeUI()
        {
            // Set page title
            if(_groupName != "")
            {
                _group = await Common.GetGroup(Common.baseUrl, _authToken.access_token, _groupName);
                PageName.Text = $"{_groupName} Passwords";
                RequestButton.Visibility = Visibility.Visible;
                SettingsButton.Visibility = Visibility.Visible;
                Description.Text = $"Group: {_groupName} • You are a {(_isManager ? "manager" : "member")}\n{_group.Description}";
            }
            else
            {
                PageName.Text = "Your Passwords";
                Description.Text = "Your work to keep your passwords strong \nOur to keep them safe";
                RequestButton.Visibility = Visibility.Collapsed;
                SettingsButton.Visibility = Visibility.Collapsed;
                PasswordsListBox.Visibility = Visibility.Visible;
            }
            
        }

        private async void LoadPasswordsAsync()
        {
            try
            { // Show loading indicator if you have one //LoadingIndicator.Visibility = Visibility.Visible; if (_groupName != "") { GroupResponse group = await Common.GetGroup(Common.baseUrl, _authToken.access_token, _groupName); foreach(var password in group.SharedPasswords) { Password pass = new Password(); pass.Shared = true; pass.Value = password.Password; pass.Name = password.Name; _passwords.Passwords.Add(pass); } } else { // Get passwords from the server _passwords = await Common.GetPasswords(Common.baseUrl, _authToken.access_token); }

                // Clear existing items
                //PasswordsListBox.Items.Clear();
                if (_groupName != "")
                {
                    // Get group passwords
                    GroupResponse group = await Common.GetGroup(Common.baseUrl, _authToken.access_token, _groupName);

                    _passwords = new PasswordListResponse();
                    _passwords.Passwords = new List<Password>();

                    // Clear any existing passwords
                    //_passwords.Passwords.Clear();
                    int i = 1;
                    // Add shared passwords from the group
                    foreach (var password in group.SharedPasswords)
                    {
                        Password pass = new Password();
                        pass.Shared = true;
                        pass.Value = password.Password;
                        pass.Name = password.Name;
                        pass.Id = i; // Make sure ID is set correctly
                        _passwords.Passwords.Add(pass);
                        i++;
                    }
                }
                else
                {
                    // Get personal passwords
                    _passwords = await Common.GetPasswords(Common.baseUrl, _authToken.access_token);
                }

                // Add items for each password
                foreach (var password in _passwords.Passwords)
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
                    iconBlock.Text = password.Name;
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
                    usernameBlock.Text = password.Value;
                    usernameBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FFaaaaaa"));
                    infoPanel.Children.Add(usernameBlock);

                    Grid.SetColumn(infoPanel, 1);
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
                    //viewButton.Style = (Style)FindResource("ModernButton");
                    viewButton.Style = this.TryFindResource("ModernButton") as Style;
                    viewButton.Tag = password.Id;
                    viewButton.Click += ViewPassword_Click;
                    buttonPanel.Children.Add(viewButton);

                    // Edit button (visible only for managers)
                    Button editButton = new Button();
                    editButton.Content = "🖊️";
                    editButton.Margin = new Thickness(0, 0, 10, 0);
                    editButton.Style = this.TryFindResource("IconButton") as Style;
                    editButton.Tag = password.Id;
                    editButton.Click += EditButton_Click;
                    if (_groupName != "") { editButton.Visibility = _isManager ? Visibility.Visible : Visibility.Collapsed; }
                    else { editButton.Visibility = Visibility.Visible; }
                    //editButton.Visibility = _isManager ? Visibility.Visible : Visibility.Collapsed;
                    buttonPanel.Children.Add(editButton);

                    // Request Edit button (visible only for members)
                    Button requestEditButton = new Button();
                    requestEditButton.Content = "📝";
                    requestEditButton.Margin = new Thickness(0, 0, 10, 0);
                    requestEditButton.Style = (Style)FindResource("RequestEditButton");
                    requestEditButton.Tag = password.Id;
                    requestEditButton.Click += RequestEditButton_Click;
                    if (_groupName != "") { requestEditButton.Visibility = _isManager ? Visibility.Collapsed : Visibility.Visible; }
                    else { requestEditButton.Visibility = Visibility.Collapsed; }
                    requestEditButton.ToolTip = "Request Edit";
                    buttonPanel.Children.Add(requestEditButton);

                    // Delete button (visible only for managers)
                    Button deleteButton = new Button();
                    deleteButton.Content = "🗑️";
                    deleteButton.Style = (Style)FindResource("IconButton");
                    deleteButton.Tag = password.Id;
                    deleteButton.Click += DeletePassword_Click;
                    if (_groupName != "") { deleteButton.Visibility = _isManager ? Visibility.Visible : Visibility.Collapsed; }
                    else { deleteButton.Visibility = Visibility.Visible; }
                    buttonPanel.Children.Add(deleteButton);

                    Grid.SetColumn(buttonPanel, 3);
                    grid.Children.Add(buttonPanel);

                    // Add the grid to a list box item
                    ListBoxItem item = new ListBoxItem();
                    item.Content = grid;
                    item.Style = this.TryFindResource("PasswordListBoxItem") as Style;

                    // Add to the list box
                    PasswordsListBox.Items.Add(item);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading passwords: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
            finally
            {
                // Hide loading indicator if you have one
                //LoadingIndicator.Visibility = Visibility.Collapsed;
            }
        }

        private void BackButton_Click(object sender, RoutedEventArgs e)
        {
            if (NavigationService != null && NavigationService.CanGoBack)
            {
                NavigationService.GoBack();
            }
        }

        private void ViewPassword_Click(object sender, RoutedEventArgs e)
        {
            // Get the button that was clicked
            Button button = sender as Button;
            if (button != null && button.Tag != null)
            {
                int passwordId = Convert.ToInt32(button.Tag);

                // Find the password
                Password selectedPassword = null;
                foreach (var password in _passwords.Passwords)
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
                    TextBlock passwordBlock = LogicalTreeHelper.FindLogicalNode(this, "passwordTextBlock" + passwordId.ToString()) as TextBlock;

                    if (passwordBlock != null)
                    {
                        // Toggle password visibility
                        if (passwordBlock.Text == "••••••••")
                        {
                            // Decrypt the password (in a real app, you'd use your encryption helper)
                            passwordBlock.Text = selectedPassword.Value; // This would be decrypted
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

       
        private void EditButton_Click(object sender, RoutedEventArgs e)
        {
            // Only managers can edit directly
            if (!_isManager && _groupName != "")
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
                Password selectedPassword = null;
                foreach (var password in _passwords.Passwords)
                {
                    if (password.Id == passwordId)
                    {
                        selectedPassword = password;
                        break;
                    }
                }

                if (selectedPassword != null)
                {
                    NavigationService?.Navigate(new AddPasswordPage(_authToken, _groupName, "upd", selectedPassword));
                }
            }
        }

        private void RequestEditButton_Click(object sender, RoutedEventArgs e)
        {
            NavigationService?.Navigate(new RequestEditPasswordDialog());
        }

        private void SettingsButton_Click(object sender, RoutedEventArgs e)
        {
            // Navigate to group settings page
            NavigationService?.Navigate(new GroupSettingsPage(_authToken, _group, _isManager, _currUser));//_groupId, _groupName, _isManager
        }

        private void RequestsButton_Click(object sender, RoutedEventArgs e)
        {
            // Only managers can view requests
            if (_isManager && _groupName != "")
            {
                // Navigate to group requests page
                NavigationService?.Navigate(new GroupRequestsPage(_authToken, _group));
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
            if (!_isManager && _groupName != "")
            {
                MessageBox.Show("Only group managers can delete passwords.",
                    "Access Denied", MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }
            else if(_isManager && _groupName != "")
            {

            }
            else
            {
                Button button = sender as Button;
                if (button != null && button.Tag != null)
                {
                    int passwordId = Convert.ToInt32(button.Tag);

                    // Find the password
                    Password selectedPassword = null;
                    foreach (var password in _passwords.Passwords)
                    {
                        if (password.Id == passwordId)
                        {
                            selectedPassword = password;
                            break;
                        }
                    }

                    if (selectedPassword != null)
                    {
                        var i = await Common.DeletePassword(Common.baseUrl, _authToken.access_token, selectedPassword.Id);
                    }
                }
            }
            return;
        }

        private void AddNewPassword_Click(object sender, RoutedEventArgs e)
        {
            // Check if user has permission to add password
            if (!_isManager && _groupName != "")
            {
                MessageBox.Show("Only group managers can add new passwords to the group.",
                    "Permission Denied", MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }

            NavigationService?.Navigate(new AddPasswordPage(_authToken, _groupName, "add", null));
        }

        public void ViewGroupRequests_Click(object sender, RoutedEventArgs e)
        {
            NavigationService?.Navigate(new GroupRequestsPage(_authToken, _group));
        }
    }
}
