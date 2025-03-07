using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
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

    public partial class GroupsPage : Page
    {
        public GroupsPage()
        {
            InitializeComponent();
            
            LoadGroups();
        }

        private void LoadGroups()
        {
            
        }

        private void ViewGroupPasswords_Click(object sender, RoutedEventArgs e)
        {
            if (sender is Button clickedButton){ NavigationService.Navigate(new PasswordsPage(clickedButton.Content.ToString()));}
            else { MessageBox.Show("Ops something went wronk"); }
        }

        private void CreateNewGroup_Click(object sender, RoutedEventArgs e)
        {
            NavigationService nav = NavigationService.GetNavigationService(this);
            nav.Navigate(new AddGroupPage());
        }

        private void GroupsListView_SelectionChanged(object sender, System.Windows.Controls.SelectionChangedEventArgs e)
        {
            /*if (GroupsListView.SelectedItem != null)
            {
                var selectedGroup = GroupsListView.SelectedItem as Group;
                //GroupDetailsPage groupDetailsPage = new GroupDetailsPage(_passwordManager, selectedGroup);
                //groupDetailsPage.Show();
                myFrame.Navigate(new GroupDetailsPage(selectedGroup));
            }*/
        }
    }
}
