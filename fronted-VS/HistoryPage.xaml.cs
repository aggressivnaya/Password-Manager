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

                    ColumnDefinition col1 = new ColumnDefinition { Width = GridLength.Auto };
                    ColumnDefinition col2 = new ColumnDefinition { Width = new GridLength(2, GridUnitType.Star) };
                    ColumnDefinition col3 = new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) };
                    ColumnDefinition col4 = new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) };
                    ColumnDefinition col5 = new ColumnDefinition { Width = new GridLength(2, GridUnitType.Star) };

                    grid.ColumnDefinitions.Add(col1);
                    grid.ColumnDefinitions.Add(col2);
                    grid.ColumnDefinitions.Add(col3);
                    grid.ColumnDefinitions.Add(col4);
                    grid.ColumnDefinitions.Add(col5);

                    // ID
                    TextBlock idBlock = new TextBlock
                    {
                        Text = historyItem.Id.ToString(),
                        Margin = new Thickness(0, 0, 15, 0)
                    };
                    Grid.SetColumn(idBlock, 0);
                    grid.Children.Add(idBlock);

                    // Password Name
                    TextBlock nameBlock = new TextBlock
                    {
                        Text = historyItem.Name,
                        FontWeight = FontWeights.SemiBold
                    };
                    Grid.SetColumn(nameBlock, 1);
                    grid.Children.Add(nameBlock);

                    // Version
                    TextBlock versionBlock = new TextBlock
                    {
                        Text = historyItem.VersionId.ToString()
                    };
                    Grid.SetColumn(versionBlock, 2);
                    grid.Children.Add(versionBlock);

                    // Method (Action)
                    TextBlock methodBlock = new TextBlock
                    {
                        Text = historyItem.Method
                    };

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

                    Grid.SetColumn(methodBlock, 3);
                    grid.Children.Add(methodBlock);

                    // Date
                    TextBlock dateBlock = new TextBlock
                    {
                        Text = historyItem.Date
                    };
                    Grid.SetColumn(dateBlock, 4);
                    grid.Children.Add(dateBlock);

                    // Add the grid to a list box item
                    ListBoxItem item = new ListBoxItem
                    {
                        Content = grid
                    };

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
