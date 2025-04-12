using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Text.Json;
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
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Net.Http.Formatting;
using Newtonsoft.Json.Linq;

namespace password_manager
{
    public partial class LoginPage : Page
    {
        //private PasswordManager _passwordManager;
        private Common _communicator;

        public LoginPage()
        {
            InitializeComponent();
           // _passwordManager = new PasswordManager();
            _communicator = new Common();
        }

        //private void NavigationService_Navigating(object sender, NavigatingCancelEventArgs e) { }

        private async void LoginButton_Click(object sender, RoutedEventArgs e)
        {
            //string email = EmailTextBox.Text;
            //string username = UsernameTextBox.Text;
            string email = "user1@example.com";
            string username = "user1";
            //string email = "q1@";
            //string username = "q1";

            if (email == null || username == null)
            {
                MessageBox.Show("username or email are empty",
                    "Access Denied", MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }

            //User user = new User(username, email);
            Token token = await Common.Login(Common.baseUrl, username, email);
            if (token != null)
            {
                Console.WriteLine($"Login successful! Token: {token.access_token}");
            }

            NavigationService nav = NavigationService.GetNavigationService(this);
            nav.Navigate(new UserDashboardPage(token, username));

        }

        private async void SignupButton_Click(object sender, RoutedEventArgs e)
        {
            // Handle signup logic or show a signup window here.  {'username': 'q1', 'email': 'q1@', 'exp': 1744561312}
            //string email = EmailTextBox.Text;
            //string username = UsernameTextBox.Text;
            string email = "q1@";
            string username = "q1";
            if (email == null || username == null)
            {
                MessageBox.Show("username or email are empty",
                    "Access Denied", MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }
            
            Token token = await Common.Signup(Common.baseUrl ,username, email);
            if (token != null)
            {
                Console.WriteLine($"Signup successful! Token: {token.access_token}");
            }
            
            NavigationService nav = NavigationService.GetNavigationService(this);
            nav.Navigate(new UserDashboardPage(token, username));
        }

        private void CloseButton_Click(object sender, RoutedEventArgs e)
        {

        }

        private void Grid_MouseLeftButtonDown(object sender, RoutedEventArgs e)
        {

        }

    }
}
