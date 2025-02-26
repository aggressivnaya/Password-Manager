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
        private PasswordManager _passwordManager;

        public GroupsPage(PasswordManager passwordManager)
        {
            InitializeComponent();
            _passwordManager = passwordManager;
            LoadGroups();
        }

        private void LoadGroups()
        {
            var groups = _passwordManager.GetGroups();
            GroupsListView.ItemsSource = groups;
        }

        private void GroupsListView_SelectionChanged(object sender, System.Windows.Controls.SelectionChangedEventArgs e)
        {
            if (GroupsListView.SelectedItem != null)
            {
                var selectedGroup = GroupsListView.SelectedItem as Group;
                //GroupDetailsPage groupDetailsPage = new GroupDetailsPage(_passwordManager, selectedGroup);
                //groupDetailsPage.Show();
                myFrame.Navigate(new GroupDetailsPage(_passwordManager, selectedGroup));
            }
        }
    }
}
