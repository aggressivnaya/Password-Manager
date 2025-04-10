using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Text.RegularExpressions;

namespace password_manager
{
    
    public partial class UserDashboardPage : Page
    {
        private Token _authToken;
        private string _currUser;

        public UserDashboardPage(Token token, string username)
        {
            InitializeComponent();

            //LoadPrivatePasswords();
            this._authToken = token;
            _currUser = username;
        }

        /*private async void LoadPrivatePasswords()
        {
           // PasswordListResponse passwords = await Common.GetPasswords(Common.baseUrl, token.access_token);
            
        }*/

        private void ViewGroupsButton_Click(object sender, RoutedEventArgs e)
        {
            //BackgroundImage.Visibility = Visibility.Collapsed;
            NavigationService nav = NavigationService.GetNavigationService(this);
            nav.Navigate(new GroupsPage(_authToken, _currUser));
        }

        private void LogoutButton_Click(object sender, RoutedEventArgs e)
        {
            //_passwordManager.Logout();
            /*myFrame.Navigate(new MainWindow());
            LoginPage loginWindow = new LoginPage();
            loginWindow.Show();
            this.Close();*/
        }

        private void CloseButton_Click(object sender, RoutedEventArgs e)
        {
            Window parentWindow = Window.GetWindow(this);
            if (parentWindow != null)
            {
                parentWindow.Close(); // Closes the window
            }
        }

        private void MaximizeButton_Click(object sender, RoutedEventArgs e)
        {
            Window parentWindow = Window.GetWindow(this); // Get the parent window
            if (parentWindow != null)
            {
                parentWindow.WindowState = (parentWindow.WindowState == WindowState.Maximized) ? WindowState.Normal : WindowState.Maximized;
            }
        }

        private void MinimizeButton_Click(object sender, RoutedEventArgs e)
        {
            Window parentWindow = Window.GetWindow(this); // Get the parent window
            if (parentWindow != null)
            {
                parentWindow.WindowState = WindowState.Minimized;
            }
        }

        private void Grid_MouseLeftButtonDown(object sender, RoutedEventArgs e)
        {
            // Allow dragging the window from the top bar
            Window parentWindow = Window.GetWindow(this);
            if (parentWindow != null)
            {
                parentWindow.DragMove();
            }
        }

        //NO NEED FOR THIS
        /*private void GetAllPasswordsPage(object sender, RoutedEventArgs e)
        {
            //NavigationService nav = NavigationService.GetNavigationService(this);
            //nav.Navigate(new ());
            //this.myFrame.Source = nav.Navigate(new());
        }*/

        private void GetPrivatePasswordsPage(object sender, RoutedEventArgs e)
        {
            BackgroundImage.Visibility = Visibility.Collapsed;
            this.myFrame.Navigate(new PasswordsPage(_authToken, "", false, _currUser));
        }

        private void GetUserGroupsPage(object sender, RoutedEventArgs e)
        {
            BackgroundImage.Visibility = Visibility.Collapsed;
            this.myFrame.Navigate(new GroupsPage(_authToken, _currUser));
        }


        // Add a method to handle group requests navigation
        private void ViewGroupRequests_Click(object sender, RoutedEventArgs e)
        {
            // Navigate to group requests page
            /*Button button = sender as Button;
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

            myFrame.Navigate(new GroupRequestsPage(_authToken, ));*/
        }

        // Add a method to join a group
        private void JoinGroup_Click(object sender, RoutedEventArgs e)
        {
            BackgroundImage.Visibility = Visibility.Collapsed;
            //Navigate to join group request page
            myFrame.Navigate(new JoinGroupRequestPage(_authToken));
        }
    }
}
