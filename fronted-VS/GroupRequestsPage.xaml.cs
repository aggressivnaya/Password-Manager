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
        private Requestts _requestts;
        
        public GroupRequestsPage(Token token, GroupResponse group)
        {
            _authToken = token;
            _groupResponse = group;
            _requestts = new Requestts();
            InitializeComponent();

            // Load requests
            LoadRequestsAsync();
        }

        private async void LoadRequestsAsync()
        {
            _requestts = await Common.GetGroupRequests(Common.baseUrl, _authToken.access_token, _groupResponse.Name);
            if (_requestts == null || _requestts.Requests == null)
                return;    
            
            // Clear existing items
            JoinRequestsListBox.Items.Clear();

            // Add items for each join request
            foreach (var request in _requestts.Requests)
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

                User user = await Common.GetUser(Common.baseUrl, _authToken.access_token);
                TextBlock nameBlock = new TextBlock();
                nameBlock.Text = user.Username;
                nameBlock.FontWeight = FontWeights.Bold;
                nameBlock.FontSize = 16;
                infoPanel.Children.Add(nameBlock);

                TextBlock typeBlock = new TextBlock();
                typeBlock.Text = $"Wants to join {_groupResponse.Name}";
                typeBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FFaaaaaa"));
                infoPanel.Children.Add(typeBlock);

                TextBlock messageBlock = new TextBlock();
                messageBlock.Text = $"Command: {request.Request_command}";
                messageBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FFaaaaaa"));
                messageBlock.TextWrapping = TextWrapping.Wrap;
                messageBlock.Margin = new Thickness(0, 5, 0, 0);
                infoPanel.Children.Add(messageBlock);

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
                acceptButton.Click += AcceptRequest_Click;
                buttonPanel.Children.Add(acceptButton);

                Button rejectButton = new Button();
                rejectButton.Content = "Reject";
                rejectButton.Style = (Style)FindResource("RejectButton");
                rejectButton.Tag = request.Id;
                rejectButton.Click += RejectRequest_Click;
                buttonPanel.Children.Add(rejectButton);

                Grid.SetColumn(buttonPanel, 2);
                grid.Children.Add(buttonPanel);

                // Add the grid to a list box item
                ListBoxItem item = new ListBoxItem();
                item.Content = grid;
                item.Style = (Style)FindResource("RequestListBoxItem");

                // Add to the list box
                JoinRequestsListBox.Items.Add(item);
            }
        }

        private void BackButton_Click(object sender, RoutedEventArgs e)
        {
            // Navigate back
            NavigationService?.GoBack();
        }

        private async void AcceptRequest_Click(object sender, RoutedEventArgs e)
        {
            // Get the button that was clicked
            Button button = sender as Button;
            if (button != null && button.Tag != null)
            {
                int requestId = Convert.ToInt32(button.Tag);

                try
                {
                    ApiResponse success = await Common.AcceptRequest(Common.baseUrl, _authToken.access_token, _groupResponse.Name, requestId);
                    if (success.Success == 200)
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
            }
        }

        private async void RejectRequest_Click(object sender, RoutedEventArgs e)
        {
            // Get the button that was clicked
            Button button = sender as Button;
            if (button != null && button.Tag != null)
            {
                int requestId = Convert.ToInt32(button.Tag);

                try
                {
                    // Reject the request
                    ApiResponse success = await Common.DeclineRequest(Common.baseUrl, _authToken.access_token, _groupResponse.Name, requestId);

                    if (success.Success == 200)
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
            }
        }
    }
}