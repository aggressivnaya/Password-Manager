using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace password_manager
{
    public partial class GroupSettingsPage : Page
    {
        private GroupResponse _group;
        private string _currUser;
        private bool _isManager;
        private Token _authToken;
        

        public GroupSettingsPage(Token token, GroupResponse group, bool isManager, string username)
        {
            InitializeComponent();

            _authToken = token;
            _group = group;
            _isManager = isManager;
            _currUser = username;

            // Initialize UI
            InitializeUI();

            // Load group members
            LoadGroupMembersAsync();
        }

        private void InitializeUI()
        {
            // Set group name
            GroupNameText.Text = $"{_group.Name} Settings";

            // Set role text
            GroupRoleText.Text = $"Your Role: {(_isManager ? "Manager" : "Member")}";
        }

        private async void LoadGroupMembersAsync()
        {
            try
            {
                // Update group info
                GroupMembersText.Text = $"{_group.Users.Count} members • {_group.SharedPasswords.Count} passwords";

                // Clear existing items
                MembersListBox.Items.Clear();

                // Add items for each member
                foreach (var member in _group.Users)
                {
                    // Create the grid layout for the member item
                    Grid grid = new Grid();

                    // Define columns
                    ColumnDefinition col1 = new ColumnDefinition();
                    col1.Width = GridLength.Auto;
                    ColumnDefinition col2 = new ColumnDefinition();
                    col2.Width = new GridLength(1, GridUnitType.Star);
                    ColumnDefinition col3 = new ColumnDefinition();
                    col3.Width = GridLength.Auto;

                    grid.ColumnDefinitions.Add(col1);
                    grid.ColumnDefinitions.Add(col2);
                    grid.ColumnDefinitions.Add(col3);

                    // Icon (crown for managers, user for members)
                    TextBlock iconBlock = new TextBlock();
                    iconBlock.Text = member.IsAdmin ? "👑" : "👤";
                    iconBlock.FontSize = 20;
                    iconBlock.Margin = new Thickness(0, 0, 15, 0);
                    Grid.SetColumn(iconBlock, 0);
                    grid.Children.Add(iconBlock);

                    // Member info
                    StackPanel infoPanel = new StackPanel();

                    TextBlock nameBlock = new TextBlock();
                    // Mark the current user
                    nameBlock.Text = member.Email == member.Email ?
                        $"You ({member.Username})" : member.Username;
                    nameBlock.FontWeight = FontWeights.Bold;
                    infoPanel.Children.Add(nameBlock);

                    TextBlock roleBlock = new TextBlock();
                    roleBlock.Text = member.IsAdmin ? "Manager" : "Member";
                    roleBlock.Foreground = new System.Windows.Media.SolidColorBrush(
                        (System.Windows.Media.Color)ColorConverter.ConvertFromString("#FFaaaaaa"));
                    infoPanel.Children.Add(roleBlock);

                    Grid.SetColumn(infoPanel, 1);
                    grid.Children.Add(infoPanel);

                    // Action buttons (only visible for managers and not for self)
                    if (_isManager && member.Email != member.Email)
                    {
                        StackPanel buttonPanel = new StackPanel();
                        buttonPanel.Orientation = Orientation.Horizontal;

                        // Make Manager button (only visible for members)
                        if (!member.IsAdmin)
                        {
                            Button makeManagerButton = new Button();
                            makeManagerButton.Content = "Make Manager";
                            makeManagerButton.Style = (Style)FindResource("ModernButton");
                            makeManagerButton.Margin = new Thickness(0, 0, 10, 0);
                            makeManagerButton.Tag = member.Id;
                            makeManagerButton.Click += MakeManager_Click;
                            buttonPanel.Children.Add(makeManagerButton);
                        }

                        // Remove button
                        Button removeButton = new Button();
                        removeButton.Content = "Remove";
                        removeButton.Style = (Style)FindResource("DangerButton");
                        removeButton.Tag = member.Id;
                        removeButton.Click += RemoveUser_Click;
                        buttonPanel.Children.Add(removeButton);

                        Grid.SetColumn(buttonPanel, 2);
                        grid.Children.Add(buttonPanel);
                    }

                    // Add the grid to a list box item
                    ListBoxItem item = new ListBoxItem();
                    item.Content = grid;

                    // Add to the list box
                    MembersListBox.Items.Add(item);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading group members: {ex.Message}",
                    "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void BackButton_Click(object sender, RoutedEventArgs e)
        {
            // Navigate back
            NavigationService?.GoBack();
        }

        private async void MakeManager_Click(object sender, RoutedEventArgs e)
        {
            // Get the button that was clicked
            Button button = sender as Button;
            if (button != null && button.Tag != null)
            {
                int memberId = Convert.ToInt32(button.Tag);

                try
                {
                    // Make the user a manager
                    //bool success = await _apiClient.MakeUserGroupManagerAsync(_authToken, _groupId, memberId);
                    bool success = true;
                    if (success)
                    {
                        // Reload members
                        LoadGroupMembersAsync();
                    }
                    else
                    {
                        MessageBox.Show("Failed to make user a manager. Please try again.",
                            "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Error making user a manager: {ex.Message}",
                        "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                }
            }
        }

        private async void RemoveUser_Click(object sender, RoutedEventArgs e)
        {
            // Get the button that was clicked
            Button button = sender as Button;
            if (button != null && button.Tag != null)
            {
                int memberId = Convert.ToInt32(button.Tag);

                // Find the member
                UserGroup selectedMember = null;
                foreach (var member in _group.Users)
                {
                    if (member.Id == memberId)
                    {
                        selectedMember = member;
                        break;
                    }
                }

                if (selectedMember != null)
                {
                    // Confirm removal
                    MessageBoxResult result = MessageBox.Show(
                        $"Are you sure you want to remove {selectedMember.Username} from the group?",
                        "Confirm Removal", MessageBoxButton.YesNo, MessageBoxImage.Warning);

                    if (result == MessageBoxResult.Yes)
                    {
                        try
                        {
                            // Remove the user
                            ApiResponse success = await Common.RemoveUser(Common.baseUrl,_authToken.access_token, _group.Name, selectedMember.Username);

                            if (success.Success == 200)
                            {
                                // Reload members
                                LoadGroupMembersAsync();
                            }
                            else
                            {
                                MessageBox.Show("Failed to remove user from group. Please try again.",
                                    "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                            }
                        }
                        catch (Exception ex)
                        {
                            MessageBox.Show($"Error removing user: {ex.Message}",
                                "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                        }
                    }
                }
            }
        }

        private async void LeaveGroup_Click(object sender, RoutedEventArgs e)
        {
            // Confirm leaving
            MessageBoxResult result = MessageBox.Show(
                "Are you sure you want to leave this group? You will lose access to all passwords.",
                "Confirm Leave Group", MessageBoxButton.YesNo, MessageBoxImage.Warning);

            if (result == MessageBoxResult.Yes)
            {
                try
                {
                    // Leave the group
                    ApiResponse success = await Common.LeaveGroup(Common.baseUrl,_authToken.access_token, _group.Name);

                    if (success.Success == 200)
                    {
                        // Navigate back to groups page
                        NavigationService?.Navigate(new GroupsPage(_authToken, _currUser));
                    }
                    else
                    {
                        MessageBox.Show("Failed to leave group. Please try again.",
                            "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Error leaving group: {ex.Message}",
                        "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                }
            }
        }
    }
}