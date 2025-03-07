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
    public partial class PasswordsPage : Page
    {
        private string groupName;
        public PasswordsPage(string groupName)
        {
            InitializeComponent();
            this.groupName = groupName;
            this.PageName.Text = (groupName == null) ? "Your Passwords" : groupName + "'s Passwords";
            this.BackButton.Visibility = (groupName == null) ? Visibility.Collapsed : Visibility.Visible;
        }

        private void BackButton_Click(object sender, RoutedEventArgs e)
        {
            if (NavigationService != null && NavigationService.CanGoBack)
            {
                NavigationService.GoBack();
            }
        }

        private void ViewPassword_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Show the password functionality to be implemented.");
        }

        private void AddNewPassword_Click(object sender, RoutedEventArgs e)
        {
            NavigationService nav = NavigationService.GetNavigationService(this);
            nav.Navigate(new AddPasswordPage());
        }
    }
}
