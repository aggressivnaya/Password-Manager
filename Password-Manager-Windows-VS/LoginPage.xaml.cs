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
    /// <summary>
    /// Interaction logic for LoginPage.xaml
    /// </summary>
    public partial class LoginPage : Page
    {
        private PasswordManager _passwordManager;

        public LoginPage()
        {
            InitializeComponent();
            _passwordManager = new PasswordManager();
        }

        //private void NavigationService_Navigating(object sender, NavigatingCancelEventArgs e) { }

        private void LoginButton_Click(object sender, RoutedEventArgs e)
        {
            string email = EmailTextBox.Text;
            string password = PasswordBox.Password;

            /*if (_passwordManager.Login(email, password))
            {
                MessageBox.Show("Login successful!");
                //UserDashboardPage dashboard = new UserDashboardPage(_passwordManager);
                //TODO: go to dashboard page
                this.myFrame.Navigate(new UserDashboardPage());
                //this.Close();
            }
            else
            {
                MessageBox.Show("Login failed. Please check your credentials.");
            }*/

            NavigationService nav = NavigationService.GetNavigationService(this);
            nav.Navigate(new UserDashboardPage());
            //this.myFrame.Navigate(new UserDashboardPage());
        }

        private void SignupButton_Click(object sender, RoutedEventArgs e)
        {
            // Handle signup logic or show a signup window here.
            MessageBox.Show("Signup functionality not yet implemented.");
            //TODO: go to dashboard page
            NavigationService nav = NavigationService.GetNavigationService(this);
            nav.Navigate(new UserDashboardPage());
        }

        private void CloseButton_Click(object sender, RoutedEventArgs e)
        {

        }

        private void Grid_MouseLeftButtonDown(object sender, RoutedEventArgs e)
        {

        }

    }
}
