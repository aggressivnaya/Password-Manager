using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace password_manager
{
    public partial class GroupRequestsPage : Page
    {
        private Token _authToken;
        private GroupResponse _groupResponse;
        
        public GroupRequestsPage(Token token, GroupResponse group)
        {
            _authToken = token;
            _groupResponse = group;
            InitializeComponent();

            // Load requests
            LoadRequestsAsync();
        }

        private async void LoadRequestsAsync()
        {
            
        }

        private void ShowJoinRequests()
        {
            // Show join requests panel, hide edit requests panel
            JoinRequestsPanel.Visibility = Visibility.Visible;
            EditRequestsPanel.Visibility = Visibility.Collapsed;

            // Clear existing items
            /*var listBox = (ListBox)FindName("JoinRequestsListBox");
            if (listBox != null)
            {
                listBox.Items.Clear();

                // Add items for each join request
                foreach (var request in _joinRequests)
                {
                    if (request.IsPending)
                    {
                        // Create the grid layout for the request item
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

                        // Icon
                        TextBlock iconBlock = new TextBlock();
                        iconBlock.Text = "👤";
                        iconBlock.FontSize = 24;
                        iconBlock.Margin = new Thickness(0, 0, 15, 0);
                        Grid.SetColumn(iconBlock, 0);
                        grid.Children.Add(iconBlock);

                        // Request info
                        StackPanel infoPanel = new StackPanel();

                        TextBlock nameBlock = new TextBlock();
                        nameBlock.Text = request.Username;
                        nameBlock.FontWeight = FontWeights.Bold;
                        nameBlock.FontSize = 16;
                        infoPanel.Children.Add(nameBlock);

                        TextBlock typeBlock = new TextBlock();
                        typeBlock.Text = $"Wants to join {request.GroupName}";
                        typeBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FFaaaaaa"));
                        infoPanel.Children.Add(typeBlock);

                        if (!string.IsNullOrEmpty(request.Message))
                        {
                            TextBlock messageBlock = new TextBlock();
                            messageBlock.Text = $"Message: {request.Message}";
                            messageBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FFaaaaaa"));
                            messageBlock.TextWrapping = TextWrapping.Wrap;
                            messageBlock.Margin = new Thickness(0, 5, 0, 0);
                            infoPanel.Children.Add(messageBlock);
                        }

                        TextBlock timeBlock = new TextBlock();
                        timeBlock.Text = $"Requested: {request.TimeAgo}";
                        timeBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FF8a8a9a"));
                        timeBlock.FontSize = 12;
                        timeBlock.Margin = new Thickness(0, 5, 0, 0);
                        infoPanel.Children.Add(timeBlock);

                        Grid.SetColumn(infoPanel, 1);
                        grid.Children.Add(infoPanel);

                        // Action buttons
                        StackPanel buttonPanel = new StackPanel();
                        buttonPanel.Orientation = Orientation.Horizontal;

                        Button acceptButton = new Button();
                        acceptButton.Content = "Accept";
                        acceptButton.Style = (Style)FindResource("AcceptButton");
                        acceptButton.Margin = new Thickness(0, 0, 10, 0);
                        acceptButton.Tag = request.Id;
                        acceptButton.Click += AcceptJoinRequest_Click;
                        buttonPanel.Children.Add(acceptButton);

                        Button rejectButton = new Button();
                        rejectButton.Content = "Reject";
                        rejectButton.Style = (Style)FindResource("RejectButton");
                        rejectButton.Tag = request.Id;
                        rejectButton.Click += RejectJoinRequest_Click;
                        buttonPanel.Children.Add(rejectButton);

                        Grid.SetColumn(buttonPanel, 2);
                        grid.Children.Add(buttonPanel);

                        // Add the grid to a list box item
                        ListBoxItem item = new ListBoxItem();
                        item.Content = grid;
                        item.Style = (Style)FindResource("RequestListBoxItem");

                        // Add to the list box
                        listBox.Items.Add(item);
                    }
                }

                // Show a message if there are no pending requests
                if (listBox.Items.Count == 0)
                {
                    TextBlock noRequestsBlock = new TextBlock();
                    noRequestsBlock.Text = "No pending join requests";
                    noRequestsBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FFaaaaaa"));
                    noRequestsBlock.HorizontalAlignment = HorizontalAlignment.Center;
                    noRequestsBlock.Margin = new Thickness(0, 20, 0, 0);

                    ListBoxItem item = new ListBoxItem();
                    item.Content = noRequestsBlock;
                    item.Background = System.Windows.Media.Brushes.Transparent;
                    item.BorderThickness = new Thickness(0);

                    listBox.Items.Add(item);
                }
            }*/
        }

        private void ShowEditRequests()
        {
            // Show edit requests panel, hide join requests panel
            /*JoinRequestsPanel.Visibility = Visibility.Collapsed;
            EditRequestsPanel.Visibility = Visibility.Visible;

            // Clear existing items
            var listBox = (ListBox)FindName("EditRequestsListBox");
            if (listBox != null)
            {
                listBox.Items.Clear();

                // Add items for each edit request
                foreach (var request in _editRequests)
                {
                    if (request.IsPending)
                    {
                        // Create the grid layout for the request item
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

                        // Icon
                        TextBlock iconBlock = new TextBlock();
                        iconBlock.Text = "🔑";
                        iconBlock.FontSize = 24;
                        iconBlock.Margin = new Thickness(0, 0, 15, 0);
                        Grid.SetColumn(iconBlock, 0);
                        grid.Children.Add(iconBlock);

                        // Request info
                        StackPanel infoPanel = new StackPanel();

                        TextBlock titleBlock = new TextBlock();
                        titleBlock.Text = "Password Edit Request";
                        titleBlock.FontWeight = FontWeights.Bold;
                        titleBlock.FontSize = 16;
                        infoPanel.Children.Add(titleBlock);

                        TextBlock userBlock = new TextBlock();
                        userBlock.Text = $"From: {request.RequestedByUsername}";
                        userBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FFaaaaaa"));
                        infoPanel.Children.Add(userBlock);

                        TextBlock passwordBlock = new TextBlock();
                        passwordBlock.Text = $"Password: {request.PasswordName}";
                        passwordBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FFaaaaaa"));
                        infoPanel.Children.Add(passwordBlock);

                        if (!string.IsNullOrEmpty(request.Reason))
                        {
                            TextBlock reasonBlock = new TextBlock();
                            reasonBlock.Text = $"Reason: {request.Reason}";
                            reasonBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FFaaaaaa"));
                            reasonBlock.TextWrapping = TextWrapping.Wrap;
                            reasonBlock.Margin = new Thickness(0, 5, 0, 0);
                            infoPanel.Children.Add(reasonBlock);
                        }

                        TextBlock timeBlock = new TextBlock();
                        timeBlock.Text = $"Requested: {request.TimeAgo}";
                        timeBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FF8a8a9a"));
                        timeBlock.FontSize = 12;
                        timeBlock.Margin = new Thickness(0, 5, 0, 0);
                        infoPanel.Children.Add(timeBlock);

                        Grid.SetColumn(infoPanel, 1);
                        grid.Children.Add(infoPanel);

                        // Action buttons
                        StackPanel buttonPanel = new StackPanel();
                        buttonPanel.Orientation = Orientation.Horizontal;

                        Button reviewButton = new Button();
                        reviewButton.Content = "Review";
                        reviewButton.Style = (Style)FindResource("ModernButton");
                        reviewButton.Margin = new Thickness(0, 0, 10, 0);
                        reviewButton.Tag = request.Id;
                        reviewButton.Click += ReviewEditRequest_Click;
                        buttonPanel.Children.Add(reviewButton);

                        Button rejectButton = new Button();
                        rejectButton.Content = "Reject";
                        rejectButton.Style = (Style)FindResource("RejectButton");
                        rejectButton.Tag = request.Id;
                        rejectButton.Click += RejectEditRequest_Click;
                        buttonPanel.Children.Add(rejectButton);

                        Grid.SetColumn(buttonPanel, 2);
                        grid.Children.Add(buttonPanel);

                        // Add the grid to a list box item
                        ListBoxItem item = new ListBoxItem();
                        item.Content = grid;
                        item.Style = (Style)FindResource("RequestListBoxItem");

                        // Add to the list box
                        listBox.Items.Add(item);
                    }
                }

                // Show a message if there are no pending requests
                if (listBox.Items.Count == 0)
                {
                    TextBlock noRequestsBlock = new TextBlock();
                    noRequestsBlock.Text = "No pending edit requests";
                    noRequestsBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FFaaaaaa"));
                    noRequestsBlock.HorizontalAlignment = HorizontalAlignment.Center;
                    noRequestsBlock.Margin = new Thickness(0, 20, 0, 0);

                    ListBoxItem item = new ListBoxItem();
                    item.Content = noRequestsBlock;
                    item.Background = System.Windows.Media.Brushes.Transparent;
                    item.BorderThickness = new Thickness(0);

                    listBox.Items.Add(item);
                }
            }*/
        }

        private void BackButton_Click(object sender, RoutedEventArgs e)
        {
            // Navigate back
            NavigationService?.GoBack();
        }

        private void JoinRequestsTab_Click(object sender, RoutedEventArgs e)
        {
            ShowJoinRequests();
        }

        private void EditRequestsTab_Click(object sender, RoutedEventArgs e)
        {
            ShowEditRequests();
        }

        private async void AcceptJoinRequest_Click(object sender, RoutedEventArgs e)
        {
            // Get the button that was clicked
            /*Button button = sender as Button;
            if (button != null && button.Tag != null)
            {
                int requestId = Convert.ToInt32(button.Tag);

                try
                {
                    // Accept the request
                    bool success = await _apiClient.RespondToGroupRequestAsync(_authToken, requestId, true);

                    if (success)
                    {
                        // Reload requests
                        LoadRequestsAsync();
                    }
                    else
                    {
                        MessageBox.Show("Failed to accept the request. Please try again.",
                            "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Error accepting request: {ex.Message}",
                        "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                }
            }*/
        }

        private async void RejectJoinRequest_Click(object sender, RoutedEventArgs e)
        {
            // Get the button that was clicked
            /*Button button = sender as Button;
            if (button != null && button.Tag != null)
            {
                int requestId = Convert.ToInt32(button.Tag);

                try
                {
                    // Reject the request
                    bool success = await _apiClient.RespondToGroupRequestAsync(_authToken, requestId, false);

                    if (success)
                    {
                        // Reload requests
                        LoadRequestsAsync();
                    }
                    else
                    {
                        MessageBox.Show("Failed to reject the request. Please try again.",
                            "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Error rejecting request: {ex.Message}",
                        "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                }
            }*/
        }

        private void ReviewEditRequest_Click(object sender, RoutedEventArgs e)
        {
            // Get the button that was clicked
            /*Button button = sender as Button;
            if (button != null && button.Tag != null)
            {
                int requestId = Convert.ToInt32(button.Tag);

                // Find the request
                PasswordEditRequestItem selectedRequest = null;
                foreach (var request in _editRequests)
                {
                    if (request.Id == requestId)
                    {
                        selectedRequest = request;
                        break;
                    }
                }

                if (selectedRequest != null)
                {
                    // TODO: Navigate to password edit review page
                    // For now, just show a message
                    MessageBox.Show($"Reviewing edit request for {selectedRequest.PasswordName}.",
                        "Review Request", MessageBoxButton.OK, MessageBoxImage.Information);
                }
            }*/
        }

        private async void RejectEditRequest_Click(object sender, RoutedEventArgs e)
        {
            // Get the button that was clicked
            /*Button button = sender as Button;
            if (button != null && button.Tag != null)
            {
                int requestId = Convert.ToInt32(button.Tag);

                // Find the request
                PasswordEditRequestItem selectedRequest = null;
                foreach (var request in _editRequests)
                {
                    if (request.Id == requestId)
                    {
                        selectedRequest = request;
                        break;
                    }
                }

                if (selectedRequest != null)
                {
                    try
                    {
                        // TODO: Implement actual API call to reject edit request
                        // For now, just show a message
                        MessageBox.Show($"Edit request for {selectedRequest.PasswordName} has been rejected.",
                            "Request Rejected", MessageBoxButton.OK, MessageBoxImage.Information);

                        // Reload requests
                        LoadRequestsAsync();
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Error rejecting request: {ex.Message}",
                            "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                }
            }*/
        }
    }
}