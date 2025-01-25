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
    public partial class GroupDetailsPage : Page
    {
        private PasswordManager _passwordManager;
        private Group _group;

        public GroupDetailsPage(PasswordManager passwordManager, Group group)
        {
            InitializeComponent();
            _passwordManager = passwordManager;
            _group = group;
            LoadGroupPasswords();
        }

        private void LoadGroupPasswords()
        {
            var passwords = _passwordManager.GetGroupPasswords(_group.GroupName);
            GroupPasswordsList.ItemsSource = passwords;
        }
    }
}
