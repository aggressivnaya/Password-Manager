using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace password_manager
{
    /// <summary>
    /// Interaction logic for GroupSettingsPage.xaml
    /// </summary>
    public partial class GroupSettingsPage : Page
    {
        private bool _isManager = false;
        private string _groupName = "Work Team";

        public GroupSettingsPage()
        {
            InitializeComponent();
            InitializeUI();
        }

        public GroupSettingsPage(string groupName, bool isManager = false)
        {
            InitializeComponent();
            _groupName = groupName;
            _isManager = isManager;
            InitializeUI();
        }

        private void InitializeUI()
        {
            // Set page title
            GroupNameText.Text = $"{_groupName} Settings";
            
            // Set role text
            GroupRoleText.Text = $"Your Role: {(_isManager ? "Manager" : "Member")}";
            
            // If user is not a manager, disable management functions
            if (!_isManager)
            {
                // Find all buttons except the Leave Group button and disable them
                foreach (UIElement element in LogicalTreeHelper.GetChildren(this))
                {
                    if (element is Grid grid)
                    {
                        DisableManagementButtons(grid);
                    }
                }
            }
        }

        private void DisableManagementButtons(DependencyObject parent)
        {
            foreach (object child in LogicalTreeHelper.GetChildren(parent))
            {
                if (child is Button button && 
                    button.Content.ToString() != "Leave Group" && 
                    button.Content.ToString() != "⬅️")
                {
                    button.IsEnabled = false;
                    button.ToolTip = "Only managers can perform this action";
                }
                else if (child is DependencyObject depObj)
                {
                    DisableManagementButtons(depObj);
                }
            }
        }

        private void BackButton_Click(object sender, RoutedEventArgs e)
        {
            // Navigate back
            NavigationService?.GoBack();
        }

        private void MakeManager_Click(object sender, RoutedEventArgs e)
        {
            // Get the button that was clicked
            Button button = (Button)sender;
            
            // Find the parent grid
            Grid parentGrid = FindParent<Grid>(button);
            
            if (parentGrid != null)
            {
                // Find the user name TextBlock in the grid
                TextBlock userNameBlock = FindChild<TextBlock>(parentGrid, block => block.FontWeight == FontWeights.Bold);
                string userName = userNameBlock?.Text ?? "User";

                // Confirm action
                MessageBoxResult result = MessageBox.Show($"Are you sure you want to make {userName} a manager of this group?", 
                    "Confirm Action", MessageBoxButton.YesNo, MessageBoxImage.Question);
                
                if (result == MessageBoxResult.Yes)
                {
                    try
                    {
                        // TODO: Implement actual database logic to update user role
                        
                        MessageBox.Show($"{userName} is now a manager of the group.", 
                            "Role Updated", MessageBoxButton.OK, MessageBoxImage.Information);
                        
                        // Update UI to reflect the change
                        // Find the role TextBlock
                        TextBlock roleBlock = FindChild<TextBlock>(parentGrid, block => block.Text == "Member");
                        if (roleBlock != null)
                        {
                            roleBlock.Text = "Manager";
                        }
                        
                        // Find the icon TextBlock
                        TextBlock iconBlock = FindChild<TextBlock>(parentGrid, block => block.Text == "👤");
                        if (iconBlock != null)
                        {
                            iconBlock.Text = "👑";
                        }
                        
                        // Hide the Make Manager button
                        button.Visibility = Visibility.Collapsed;
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Error updating role: {ex.Message}", 
                            "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                }
            }
        }

        private void RemoveUser_Click(object sender, RoutedEventArgs e)
        {
            // Get the button that was clicked
            Button button = (Button)sender;
            
            // Find the parent grid
            Grid parentGrid = FindParent<Grid>(button);
            
            if (parentGrid != null)
            {
                // Find the user name TextBlock in the grid
                TextBlock userNameBlock = FindChild<TextBlock>(parentGrid, block => block.FontWeight == FontWeights.Bold);
                string userName = userNameBlock?.Text ?? "User";

                // Confirm removal
                MessageBoxResult result = MessageBox.Show($"Are you sure you want to remove {userName} from this group?", 
                    "Confirm Removal", MessageBoxButton.YesNo, MessageBoxImage.Warning);
                
                if (result == MessageBoxResult.Yes)
                {
                    try
                    {
                        // TODO: Implement actual database logic to remove user from group
                        
                        MessageBox.Show($"{userName} has been removed from the group.", 
                            "User Removed", MessageBoxButton.OK, MessageBoxImage.Information);
                        
                        // Remove the item from the list
                        ListBoxItem item = FindParent<ListBoxItem>(parentGrid);
                        if (item != null)
                        {
                            ListBox listBox = (ListBox)item.Parent;
                            listBox.Items.Remove(item);
                        }
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Error removing user: {ex.Message}", 
                            "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                }
            }
        }

        private void LeaveGroup_Click(object sender, RoutedEventArgs e)
        {
            // Confirm leaving group
            MessageBoxResult result = MessageBox.Show($"Are you sure you want to leave the {_groupName} group?", 
                "Confirm Leave Group", MessageBoxButton.YesNo, MessageBoxImage.Warning);
            
            if (result == MessageBoxResult.Yes)
            {
                try
                {
                    // TODO: Implement actual database logic to remove user from group
                    
                    MessageBox.Show($"You have left the {_groupName} group.", 
                        "Group Left", MessageBoxButton.OK, MessageBoxImage.Information);
                    
                    // Navigate back to groups page
                    // Assuming we need to go back twice to reach the groups page
                    NavigationService?.GoBack();
                    NavigationService?.GoBack();
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Error leaving group: {ex.Message}", 
                        "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                }
            }
        }

        // Helper method to find parent of a specific type
        private static T FindParent<T>(DependencyObject child) where T : DependencyObject
        {
            DependencyObject parentObject = VisualTreeHelper.GetParent(child);

            if (parentObject == null)
                return null;

            T parent = parentObject as T;
            if (parent != null)
                return parent;
            else
                return FindParent<T>(parentObject);
        }

        // Helper method to find child of a specific type with a condition
        private static T FindChild<T>(DependencyObject parent, Func<T, bool> condition) where T : DependencyObject
        {
            int childCount = VisualTreeHelper.GetChildrenCount(parent);
            for (int i = 0; i < childCount; i++)
            {
                DependencyObject child = VisualTreeHelper.GetChild(parent, i);
                
                T childType = child as T;
                if (childType != null && condition(childType))
                    return childType;

                T foundChild = FindChild<T>(child, condition);
                if (foundChild != null)
                    return foundChild;
            }
            return null;
        }
    }
}