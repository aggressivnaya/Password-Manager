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
using password_manager.Models;

namespace password_manager
{

    public partial class GroupsPage : Page
    {
        private Common _apiClient;
        //private List<GroupItem> _groups;
        private string _authToken;

        public GroupsPage()
        {
            InitializeComponent();

            // Get the API client
            _apiClient = new Common();

            // Get the auth token from session manager
            //_authToken = SessionManager.Instance.AuthToken;

            // Load groups
            //LoadGroupsAsync();
        }

        /*private async void LoadGroupsAsync()
        {
            try
            {
                // Show loading indicator if you have one
                // LoadingIndicator.Visibility = Visibility.Visible;

                // Get groups from the server
                //_groups = await _apiClient.GetUserGroupsAsync(_authToken);
                //_groups = null;

                // Clear existing items
                var listBox = (ListBox)FindName("GroupsListBox");
                if (listBox != null)
                {
                    listBox.Items.Clear();

                    // Add items for each group
                    foreach (var group in _groups)
                    {
                        // Create the grid layout for the group item
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
                        iconBlock.Text = group.Icon;
                        iconBlock.FontSize = 24;
                        iconBlock.Margin = new Thickness(0, 0, 15, 0);
                        Grid.SetColumn(iconBlock, 0);
                        grid.Children.Add(iconBlock);

                        // Group info
                        StackPanel infoPanel = new StackPanel();

                        TextBlock nameBlock = new TextBlock();
                        nameBlock.Text = group.Name;
                        nameBlock.FontWeight = FontWeights.Bold;
                        nameBlock.FontSize = 18;
                        infoPanel.Children.Add(nameBlock);

                        TextBlock detailsBlock = new TextBlock();
                        detailsBlock.Text = group.Info;
                        detailsBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FFaaaaaa"));
                        infoPanel.Children.Add(detailsBlock);

                        Grid.SetColumn(infoPanel, 1);
                        grid.Children.Add(infoPanel);

                        // View button
                        Button viewButton = new Button();
                        viewButton.Content = "View";
                        viewButton.Style = (Style)FindResource("ModernButton");
                        viewButton.Tag = group.Id;
                        viewButton.Click += ViewGroupPasswords_Click;
                        Grid.SetColumn(viewButton, 2);
                        grid.Children.Add(viewButton);

                        // Add the grid to a list box item
                        ListBoxItem item = new ListBoxItem();
                        item.Content = grid;
                        item.Style = (Style)FindResource("GroupListBoxItem");

                        // Add to the list box
                        listBox.Items.Add(item);
                    }
                }

                // Check if there are pending requests for any groups where the user is a manager
                /*bool hasPendingRequests = false;
                foreach (var group in _groups)
                {
                    if (group.IsManager)
                    {
                        var requests = await _apiClient.GetPendingGroupRequestsAsync(_authToken, group.Id);
                        if (requests.Count > 0)
                        {
                            hasPendingRequests = true;
                            break;
                        }
                    }
                }*/

        // Show/hide the requests button
        //ViewRequestsButton.Visibility = hasPendingRequests ? Visibility.Visible : Visibility.Collapsed;
        //}
        //catch (Exception ex)
        //{
        //  MessageBox.Show($"Error loading groups: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
        //}
        //finally
        //{
        // Hide loading indicator if you have one
        // LoadingIndicator.Visibility = Visibility.Collapsed;
        //}
        // }*/

        private void ViewGroupPasswords_Click(object sender, RoutedEventArgs e)
        {
            NavigationService?.Navigate(new PasswordsPage(1, "name", true));
        }
        private void CreateNewGroup_Click(object sender, RoutedEventArgs e)
        {
            // TODO: Navigate to create group page
            // For now, just show a message
            MessageBox.Show("Creating a new group.",
                "Create Group", MessageBoxButton.OK, MessageBoxImage.Information);
            NavigationService nav = NavigationService.GetNavigationService(this);
            nav.Navigate(new AddGroupPage());
        }

        // Add a new method to handle joining an existing group
        public void JoinExistingGroup_Click(object sender, RoutedEventArgs e)
        {
            // Navigate to join group request page
            NavigationService?.Navigate(new JoinGroupRequestPage());
        }

        public void ViewGroupRequests_Click(object sender, RoutedEventArgs e)
        {
            // Find a group where the user is a manager
            NavigationService?.Navigate(new GroupRequestsPage(1));
        }
    }
}
