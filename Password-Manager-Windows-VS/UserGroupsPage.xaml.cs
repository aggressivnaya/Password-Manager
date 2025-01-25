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
    public partial class UserGroupsPage : Page
    {
        public UserGroupsPage()
        {
            InitializeComponent();
        }

        private void ViewGroupPasswords_Click(object sender, RoutedEventArgs e)
        {
            // Navigate to the GroupPasswordsPage
            // You would typically pass the group information here
            NavigationService.Navigate(new GroupPasswordsPage());
        }

        private void CreateNewGroup_Click(object sender, RoutedEventArgs e)
        {
            // Implement the logic to create a new group
            MessageBox.Show("Create New Group functionality to be implemented.");
        }
    }
}
