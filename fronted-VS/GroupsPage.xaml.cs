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

    public partial class GroupsPage : Page
    {
        private Token _authToken;
        private GroupListResponse _groups;
        private string _currUser;

        public GroupsPage(Token token,string username)
        {
            InitializeComponent();

            _authToken = token;
            _currUser = username;
            // Get the auth token from session manager
            //_authToken = SessionManager.Instance.AuthToken;

            // Load groups
            LoadGroupsAsync();
        }

        private async void LoadGroupsAsync()
        {
            try
            {
                // Show loading indicator if you have one
                // LoadingIndicator.Visibility = Visibility.Visible;

                // Get groups from the server
                _groups = await Common.GetGroups(Common.baseUrl, _authToken.access_token);

                //_groups = null;

                GroupsListBox.Items.Clear();

                // Add items for each group
                foreach (var group in _groups.Groups)
                {
                    GroupResponse requestedGroup = await Common.GetGroup(Common.baseUrl, _authToken.access_token, group);
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
                    iconBlock.Text = requestedGroup.Name;
                    iconBlock.FontSize = 24;
                    iconBlock.Margin = new Thickness(0, 0, 15, 0);
                    Grid.SetColumn(iconBlock, 0);
                    grid.Children.Add(iconBlock);

                    // Group info
                    StackPanel infoPanel = new StackPanel();

                    TextBlock nameBlock = new TextBlock();
                    nameBlock.Text = requestedGroup.Name;
                    nameBlock.FontWeight = FontWeights.Bold;
                    nameBlock.FontSize = 18;
                    infoPanel.Children.Add(nameBlock);

                    TextBlock detailsBlock = new TextBlock();
                    detailsBlock.Text = requestedGroup.Description;
                    detailsBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FFaaaaaa"));
                    infoPanel.Children.Add(detailsBlock);

                    Grid.SetColumn(infoPanel, 1);
                    grid.Children.Add(infoPanel);

                    // View button
                    Button viewButton = new Button();
                    viewButton.Content = "View";
                    viewButton.Style = (Style)FindResource("ModernButton");
                    viewButton.Tag = requestedGroup.Name;
                    viewButton.Click += ViewGroupPasswords_Click;
                    Grid.SetColumn(viewButton, 2);
                    grid.Children.Add(viewButton);

                    // Add the grid to a list box item
                    ListBoxItem item = new ListBoxItem();
                    item.Content = grid;
                    item.Style = (Style)FindResource("GroupListBoxItem");

                    // Add to the list box
                    GroupsListBox.Items.Add(item);
                }

                // Check if there are pending requests for any groups where the user is a manager
                bool hasPendingRequests = false;
                /*foreach (var group in _groups.Groups)
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
                ViewRequestsButton.Visibility = hasPendingRequests ? Visibility.Visible : Visibility.Collapsed;
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading groups: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
            finally
            {
                //Hide loading indicator if you have one
                //LoadingIndicator.Visibility = Visibility.Collapsed;
            }
        }

        private void ViewGroupPasswords_Click(object sender, RoutedEventArgs e)
        {
            Button button = sender as Button;
            if (button != null && button.Tag != null)
            {
                string groupId = button.Tag.ToString();

                // Find the group
                GroupResponse selectedGroup = new GroupResponse();
                foreach (var group in _groups.Groups)
                {
                    if (group == groupId)
                    {
                        selectedGroup.Name = group;
                        break;
                    }
                }
                NavigationService?.Navigate(new PasswordsPage(_authToken, selectedGroup.Name, true, _currUser));

                /*foreach (var user in selectedGroup.Users)
                {
                    if (user.Username == _currUser)
                    {
                        NavigationService?.Navigate(new PasswordsPage(_authToken, selectedGroup.Name, true, _currUser));
                    }
                }*/
            }
                
        }
        private void CreateNewGroup_Click(object sender, RoutedEventArgs e)
        {
            NavigationService nav = NavigationService.GetNavigationService(this);
            nav.Navigate(new AddGroupPage(_authToken));
        }

        // Add a new method to handle joining an existing group
        public void JoinExistingGroup_Click(object sender, RoutedEventArgs e)
        {
            // Navigate to join group request page
            NavigationService?.Navigate(new JoinGroupRequestPage(_authToken));
        }

        public async void ViewGroupRequests_Click(object sender, RoutedEventArgs e)
        {
            // Find a group where the user is a manager
            Button button = sender as Button;
            if (button != null && button.Tag != null)
            {
                string groupId = button.Tag.ToString();

                // Find the group
                GroupResponse selectedGroup = null;
                foreach (var group in _groups.Groups)
                {
                    if (group == groupId)
                    {
                        selectedGroup = await Common.GetGroup(Common.baseUrl, _authToken.access_token, group);
                        break;
                    }
                }


                NavigationService?.Navigate(new GroupRequestsPage(_authToken, selectedGroup));
            }
        }
    }
}
