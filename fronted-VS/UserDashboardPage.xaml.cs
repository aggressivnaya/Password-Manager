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

namespace password_manager
{
    
    public partial class UserDashboardPage : Page
    {
        //private PasswordManager _passwordManager;

        public UserDashboardPage()
        {
            InitializeComponent();
            //_passwordManager = passwordManager;
            LoadPrivatePasswords();
        }

        private void LoadPrivatePasswords()
        {
            //var passwords = _passwordManager.GetPrivatePasswords();
            //PrivatePasswordsList.ItemsSource = passwords;
        }

        private void ViewGroupsButton_Click(object sender, RoutedEventArgs e)
        {
            NavigationService nav = NavigationService.GetNavigationService(this);
            nav.Navigate(new GroupsPage());
        }

        private void LogoutButton_Click(object sender, RoutedEventArgs e)
        {
            //_passwordManager.Logout();
            //myFrame.Navigate(new MainWindow());
            //LoginPage loginWindow = new LoginPage();
            //loginWindow.Show();
            //this.Close();
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
        private void GetAllPasswordsPage(object sender, RoutedEventArgs e)
        {
            //NavigationService nav = NavigationService.GetNavigationService(this);
            //nav.Navigate(new ());
            //this.myFrame.Source = nav.Navigate(new());
        }

        private void GetPrivatePasswordsPage(object sender, RoutedEventArgs e)
        {
            this.myFrame.Navigate(new PasswordsPage(1, "name", true));
        }

        /*private void GetUserGroupsPage(object sender, RoutedEventArgs e)
        {
            this.myFrame.Navigate(new GroupsPage());
        }*/

        private void GetUserGroupsPage(object sender, RoutedEventArgs e)
        {
            // Navigate to the groups page
            myFrame.Navigate(new GroupsPage());
        }

        // Add a method to handle group requests navigation
        private void ViewGroupRequests_Click(object sender, RoutedEventArgs e)
        {
            // Navigate to group requests page
            myFrame.Navigate(new GroupRequestsPage(1));
        }

        // Add a method to join a group
        private void JoinGroup_Click(object sender, RoutedEventArgs e)
        {
            // Navigate to join group request page
            myFrame.Navigate(new JoinGroupRequestPage());
        }
    }
}
