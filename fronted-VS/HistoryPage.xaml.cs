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
    /// <summary>
    /// Interaction logic for HistoryPage.xaml
    /// </summary>
    public partial class HistoryPage : Page
    {
        private Token _authToken;
        private HistoryResponse _historyItems;
        public HistoryPage(Token token)
        {
            _authToken = token;
            _historyItems = new HistoryResponse();
            _historyItems.History = new List<HistoryItem>();
            InitializeComponent();
            LoadHistoryAsync();
        }

        private async void LoadHistoryAsync()
        {
            try
            {
                // Get groups from the server
                _historyItems = await Common.GetHistory(Common.baseUrl, _authToken.access_token);

                //_groups = null;

                HistoryBox.Items.Clear();

                // Add items for each group
                foreach (var historyItem in _historyItems.History)
                {
                    Grid grid = new Grid();

                    RowDefinition col1 = new RowDefinition { Height = GridLength.Auto };
                    RowDefinition col2 = new RowDefinition { Height = new GridLength(2, GridUnitType.Star) };
                    RowDefinition col3 = new RowDefinition { Height = new GridLength(1, GridUnitType.Star) };
                    RowDefinition col4 = new RowDefinition { Height = new GridLength(1, GridUnitType.Star) };

                    grid.RowDefinitions.Add(col1);
                    grid.RowDefinitions.Add(col2);
                    grid.RowDefinitions.Add(col3);
                    grid.RowDefinitions.Add(col4);

                    // Password Name
                    TextBlock nameBlock = new TextBlock
                    {
                        Text = $"Name of Password: {historyItem.Name}",
                        FontWeight = FontWeights.SemiBold
                    };
                    nameBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FFaaaaaa"));
                    nameBlock.FontWeight = FontWeights.Bold;
                    nameBlock.FontSize = 18;
                    Grid.SetRow(nameBlock, 0);
                    grid.Children.Add(nameBlock);

                    // Version
                    TextBlock versionBlock = new TextBlock
                    {
                        Text = $"Version: {historyItem.VersionId.ToString()}"
                    };
                    versionBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FFaaaaaa"));
                    versionBlock.FontWeight = FontWeights.Bold;
                    versionBlock.FontSize = 18;
                    Grid.SetRow(versionBlock, 1);
                    grid.Children.Add(versionBlock);

                    // Method (Action)
                    TextBlock methodBlock = new TextBlock
                    {
                        Text = $"Method: {historyItem.Method }"
                    };
                    versionBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FFaaaaaa"));
                    versionBlock.FontWeight = FontWeights.Bold;
                    versionBlock.FontSize = 18;

                    // Set color based on method
                    switch (historyItem.Method.ToLower())
                    {
                        case "create":
                            methodBlock.Foreground = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#FF28a745"));
                            break;
                        case "update":
                            methodBlock.Foreground = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#FF007bff"));
                            break;
                        case "delete":
                            methodBlock.Foreground = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#FFdc3545"));
                            break;
                    }
                    methodBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FFaaaaaa"));
                    methodBlock.FontWeight = FontWeights.Bold;
                    methodBlock.FontSize = 18;

                    Grid.SetRow(methodBlock, 2);
                    grid.Children.Add(methodBlock);

                    // Date
                    TextBlock dateBlock = new TextBlock
                    {
                        Text = $"Date: {historyItem.Date}"
                    };
                    dateBlock.Foreground = new System.Windows.Media.SolidColorBrush((System.Windows.Media.Color)ColorConverter.ConvertFromString("#FFaaaaaa"));
                    dateBlock.FontWeight = FontWeights.Bold;
                    dateBlock.FontSize = 18;
                    Grid.SetRow(dateBlock, 3);
                    grid.Children.Add(dateBlock);

                    // Add the grid to a list box item
                    ListBoxItem item = new ListBoxItem
                    {
                        Content = grid
                    };
                    item.Style = (Style)FindResource("GroupListBoxItem");

                    // Add to the list box
                    HistoryBox.Items.Add(item);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading history: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
            finally
            {

            }
        }
    }
}
