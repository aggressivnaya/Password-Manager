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
    /// Interaction logic for AuthenticationPage.xaml
    /// </summary>
    public partial class AuthenticationPage : Page
    {
        private Token token;
        private string user;
        public AuthenticationPage(Token token,string currUser)
        {
            this.token = token;
            this.user = currUser;
            InitializeComponent();
        }

        private async void VerifyButton_Click(object sender, RoutedEventArgs e)
        {
            string code = CodeTextBox.Text;
            if(code == null)
            {
                MessageBox.Show("code is empty",
                    "Access Denied", MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }

            ApiResponse apiResponse = await Common.CheckVerificationCode(Common.baseUrl, token.access_token, code);
            if(apiResponse == null || apiResponse.Success != 200) {
                MessageBox.Show("Ops there was some mistake",
                    "Access Denied", MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }
            
            NavigationService nav = NavigationService.GetNavigationService(this);
            nav.Navigate(new UserDashboardPage(token, user));
        }
    }
}
