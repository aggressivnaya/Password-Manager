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
    
    public partial class UserDashboardPage : Page
    {
        private PasswordManager _passwordManager;

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
            //GroupsPage groupsPage = new GroupsPage(_passwordManager);
            //groupsPage.Show();
            //TODO: go to group page
            NavigationService nav = NavigationService.GetNavigationService(this);
            nav.Navigate(new UserGroupsPage());
        }

        private void LogoutButton_Click(object sender, RoutedEventArgs e)
        {
            _passwordManager.Logout();
            //myFrame.Navigate(new MainWindow());
            //LoginPage loginWindow = new LoginPage();
            //loginWindow.Show();
            //this.Close();
        }

        private void CloseButton_Click(object sender, RoutedEventArgs e)
        {

        }
        private void MaximizeButton_Click(object sender, RoutedEventArgs e)
        {

        }
        private void MinimizeButton_Click(object sender, RoutedEventArgs e)
        {

        }
        private void Grid_MouseLeftButtonDown(object sender, RoutedEventArgs e)
        {

        }

        private void GetAllPasswordsPage(object sender, RoutedEventArgs e)
        {
            NavigationService nav = NavigationService.GetNavigationService(this);
            //nav.Navigate(new ());
        }

        private void GetPrivatePasswordsPage(object sender, RoutedEventArgs e)
        {
            int i = 0;
            NavigationService nav = NavigationService.GetNavigationService(this);
            i++;
            nav.Navigate(new GroupPasswordsPage());
        }

        private void GetSharedPasswordsPage(object sender, RoutedEventArgs e)
        {
            NavigationService nav = NavigationService.GetNavigationService(this);
            nav.Navigate(new UserGroupsPage());
        }
    }
}
