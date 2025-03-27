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
        private PasswordManager _passwordManager;
        private Common _communicator;

        public LoginPage()
        {
            InitializeComponent();
            _passwordManager = new PasswordManager();
            _communicator = new Common();
        }

        //private void NavigationService_Navigating(object sender, NavigatingCancelEventArgs e) { }

        private async Task LoginButton_Click(object sender, RoutedEventArgs e)
        {
            string email = EmailTextBox.Text;
            string username = UsernameTextBox.Text;
            User user = new User(username, email);
            string token = await _communicator.LoginAsync(user);
            if (token != null)
            {
                Console.WriteLine($"Login successful! Token: {token}");
            }

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
        }

        private async Task SignupButton_Click(object sender, RoutedEventArgs e)
        {
            // Handle signup logic or show a signup window here.
            string email = EmailTextBox.Text;
            string username = UsernameTextBox.Text;
            User user = new User(username, email);
            string token = await _communicator.SignupAsync(user);
            if (token != null)
            {
                Console.WriteLine($"Signup successful! Token: {token}");
            }
            //MessageBox.Show("Signup functionality not yet implemented.");
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

        //static async Task Main()
        //{
            

            // Sign up
            

            // Log in
            

            // Validate token
            /*if (token != null)
            {
                bool isValid = await ValidateToken(token);
                Console.WriteLine($"Token validation: {isValid}");
            }*/
        //}

    }
}
