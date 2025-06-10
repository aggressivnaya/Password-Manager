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
        private Common _communicator;

        public LoginPage()
        {
            InitializeComponent();
            _communicator = new Common();
        }

        //private void NavigationService_Navigating(object sender, NavigatingCancelEventArgs e) { }

        private async void LoginButton_Click(object sender, RoutedEventArgs e)
        {
            string email = EmailTextBox.Text;
            string username = UsernameTextBox.Text;

            if (email == null || username == null)
            {
                MessageBox.Show("username or email are empty",
                    "Access Denied", MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }

            Token token = await Common.Login(Common.baseUrl, username, email);
            if (token != null)
            {
                Console.WriteLine($"Login successful! Token: {token.access_token}");
            }

            NavigationService nav = NavigationService.GetNavigationService(this);
            nav.Navigate(new AuthenticationPage(token, username));

        }

        private async void SignupButton_Click(object sender, RoutedEventArgs e)
        {
            string email = EmailTextBox.Text;
            string username = UsernameTextBox.Text;
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
            nav.Navigate(new AuthenticationPage(token, username));
        }

        private void CloseButton_Click(object sender, RoutedEventArgs e)
        {

        }

        private void Grid_MouseLeftButtonDown(object sender, RoutedEventArgs e)
        {

        }

    }
}
