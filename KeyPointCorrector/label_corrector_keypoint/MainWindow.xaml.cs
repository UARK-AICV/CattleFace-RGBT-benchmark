using Microsoft.Win32;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.IO;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Forms;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;
using System.Xml.Linq;
using MouseEventArgs = System.Windows.Input.MouseEventArgs;

// TODO:
// - [ ] Browse button
// - [x] Load all files in folder
// - [x] Load image
// - [x] Draw 13 points
// - [x] Draw bbox
// - [x] Move points
// - [x] Move bbox
// - [x] Load label from json
// - [ ] Save label to json: after click save and move mouse. After saving, reload the json.
// - [x] Next image
// - [x] Previous image
// - [ ] set default point in a place we can reach easily to move it, in case the model doesn't detect location.



namespace label_corrector_keypoint
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        // we have 13 points and 1 bbox
        Ellipse[] kpoints = new Ellipse[13];
        Image imageMain;
        TextBlock[] textBlocks = new TextBlock[13];
        // srote current images path 
        string currentDir;
        string annotationfn = "metadata_csharp.json";
        string currentImagePath;
        List<string> all_filepath = new List<string>();
        string fn;
        JArray annotation;
        int current_index = 0;
        //Dictionary for keep or discard status
        Dictionary<string, string> Keep_or_Discard = new Dictionary<string, string>();
        Boolean start = false;
        public MainWindow()
        {
            InitializeComponent();
            this.imageMain = CanvasMain.Children[0] as Image;
            //this.TextBoxX.Text = "0";
            //this.TextBoxY.Text = "0";

        }
        UIElement dragObject = null;
        Point offset;
        TextBlock textBlock;
        
        //Method to update buttons and status based on the image's keep or discard status
        public void UpdateStatus()
        {
            JObject current_item = (JObject)annotation[current_index];
            if (Keep_or_Discard[current_item["id"].ToString()].Equals("Keep"))
            {
                TextStatus.Text = "Status: Keep";
                ButtonKorD.Content = "Discard";
            }
            else
            {
                TextStatus.Text = "Status: Discard";
                ButtonKorD.Content = "Keep";
            }
        }
        private void kpoint_PreviewMouseDown(object sender, MouseButtonEventArgs e)
        {
            this.dragObject = sender as UIElement;
            this.offset = e.GetPosition(this.CanvasMain);
            this.offset.Y -= Canvas.GetTop(this.dragObject);
            this.offset.X -= Canvas.GetLeft(this.dragObject);
            // capture mouse
            this.CanvasMain.CaptureMouse();
        }
        private void CanvasMain_PreviewMouseMove(object sender, MouseEventArgs e)
        {
            if (this.dragObject == null)
                return;
            var position = e.GetPosition(sender as IInputElement);
            Canvas.SetTop(this.dragObject, position.Y - this.offset.Y);
            Canvas.SetLeft(this.dragObject, position.X - this.offset.X);
            // move tag of kpoint too 
            Ellipse ellipse = this.dragObject as Ellipse;
            this.textBlock = ellipse.Tag as TextBlock;
            Canvas.SetTop(this.textBlock, Canvas.GetTop(this.dragObject));
            Canvas.SetLeft(this.textBlock, Canvas.GetLeft(this.dragObject) + ellipse.Width);

            Point p1 = new Point(Canvas.GetLeft(this.dragObject), Canvas.GetTop(this.dragObject));

            p1.X += ellipse.Width;
            p1.Y += ellipse.Height;
            p1.X = p1.X / this.imageMain.ActualWidth * this.imageMain.Source.Width;
            p1.Y = p1.Y / this.imageMain.ActualHeight * this.imageMain.Source.Height;

            int id = Int32.Parse(this.textBlock.Text)-1;

            JObject current_obj = (JObject)annotation[this.current_index];
            current_obj["points"][id * 3] = (int)Math.Round(p1.X);
            current_obj["points"][id*3 + 1] = (int)Math.Round(p1.Y);
            annotation[this.current_index] = (JToken)current_obj;
            //this.TextBoxX.Text = p1.X.ToString();
            //this.TextBoxY.Text = p1.Y.ToString();
        }


        private void CanvasMain_PreviewMouseUp(object sender, MouseButtonEventArgs e)
        {
            this.dragObject = null;
            this.CanvasMain.ReleaseMouseCapture();
        }

        private void ButtonReload_Click(object sender, RoutedEventArgs e)
        {
            // join path of currentImagePath and fn
            this.imageMain.Source = new BitmapImage(new Uri(System.IO.Path.Combine(this.currentImagePath, this.fn)));
            // get max resolution of screen and set it to image, scale image to fit 70% of screen
            this.imageMain.Width = this.imageMain.Source.Width;
            this.imageMain.Height = this.imageMain.Source.Height;
            double width = SystemParameters.PrimaryScreenWidth * 0.7;
            double height = SystemParameters.PrimaryScreenHeight * 0.7;
            if (this.imageMain.Width > width)
            {
                this.imageMain.Width = width;
                this.imageMain.Height = (int)width * this.imageMain.Source.Height / this.imageMain.Source.Width;
            }
            if (this.imageMain.Height > height)
            {
                this.imageMain.Height = height;
                this.imageMain.Width = height * this.imageMain.Source.Width / this.imageMain.Source.Height;
                // round it 
                this.imageMain.Width = (int)this.imageMain.Width;
            }


            // scale canvas to fit image
            this.CanvasMain.Width = this.imageMain.Width + 20;
            this.CanvasMain.Height = this.imageMain.Height + 50;
            // scale main window to fit image
            this.Width = this.CanvasMain.Width * 4 / 3;
            this.Height = this.CanvasMain.Height;
            imageMain.PreviewMouseDown += ImageMain_PreviewMouseDown;
        }

        private void ImageMain_PreviewMouseDown(object sender, MouseButtonEventArgs e)
        {
            int n = -1; 
            //check if key is pressed and correlate keypoint
            var position = e.GetPosition(sender as IInputElement);
            if (Keyboard.IsKeyDown(Key.D1))
                n = 0;
            if (Keyboard.IsKeyDown(Key.D2))
                n = 1;
            if (Keyboard.IsKeyDown(Key.D3))
                n = 2;
            if (Keyboard.IsKeyDown(Key.D4))
                n = 3;
            if (Keyboard.IsKeyDown(Key.D5))
                n = 4;
            if (Keyboard.IsKeyDown(Key.D6))
                n = 5;
            if (Keyboard.IsKeyDown(Key.D7))
                n = 6;
            if (Keyboard.IsKeyDown(Key.D8))
                n = 7;
            if (Keyboard.IsKeyDown(Key.D9))
                n = 8;
            if (Keyboard.IsKeyDown(Key.R))
                n = 9;
            if (Keyboard.IsKeyDown(Key.W))
                n = 10;
            if (Keyboard.IsKeyDown(Key.E))
                n = 11;
            if (Keyboard.IsKeyDown(Key.Q))
                n = 12;

            if (n >= 0)
            {
                //move key point
                double x_pos = position.Y - this.offset.Y - this.kpoints[n].Height/2;
                double y_pos = position.X - this.offset.X - this.kpoints[n].Width/2;
                Canvas.SetTop(this.kpoints[n], x_pos);
                Canvas.SetLeft(this.kpoints[n], y_pos);

                //move textbox
                Canvas.SetTop(this.textBlocks[n], Canvas.GetTop(this.kpoints[n]));
                Canvas.SetLeft(this.textBlocks[n], Canvas.GetLeft(this.kpoints[n]) + this.kpoints[n].Width);

                Point p1 = new Point(Canvas.GetLeft(this.kpoints[n]), Canvas.GetTop(this.kpoints[n]));


                p1.X += this.kpoints[n].Width;
                p1.Y += this.kpoints[n].Height;
                p1.X = p1.X / this.imageMain.ActualWidth * this.imageMain.Source.Width;
                p1.Y = p1.Y / this.imageMain.ActualHeight * this.imageMain.Source.Height;


                JObject current_obj = (JObject)annotation[this.current_index];
                current_obj["points"][n * 3] = (int)Math.Round(p1.X);
                current_obj["points"][n * 3 + 1] = (int)Math.Round(p1.Y);
                annotation[this.current_index] = (JToken)current_obj;
            }
        }

        private void ButtonBrowse_Click(object sender, RoutedEventArgs e)
        {
            // Current directory is hard code here
            try
            {
                FolderBrowserDialog dlg = new FolderBrowserDialog();
                
                if (dlg.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    
                    this.currentDir = dlg.SelectedPath;

                }
                start = true; 
                this.currentImagePath = System.IO.Path.Combine(this.currentDir, "images");
                this.annotationfn = System.IO.Path.Combine(this.currentDir, this.annotationfn);
                
                // load json 
                // load json a
                annotation = JArray.Parse(File.ReadAllText(this.annotationfn));
                JObject current_item;
                // get all id of images 
                for (int i = 0; i < annotation.Count; i++)
                {
                    current_item = (JObject)annotation[i];
                    Keep_or_Discard.Add(current_item["id"].ToString(), "Keep");
                    this.all_filepath.Add(System.IO.Path.Combine(this.currentImagePath, current_item["id"].ToString() + ".jpg"));
                }
                // get first image
                this.fn = System.IO.Path.GetFileName(this.all_filepath[this.current_index]);
                this.ButtonReload_Click(sender, e);

                // after load the image, load points and box
                current_item = (JObject)annotation[this.current_index];
                // parse current item to get all points
                for (int i = 0; i < 13; i++)
                {
                    // create kpoint
                    this.kpoints[i] = new Ellipse();
                    this.kpoints[i].Fill = Brushes.LightGreen;
                    this.kpoints[i].Width = 6;
                    this.kpoints[i].Height = 6;
                    double location_x = (double)current_item["points"][i * 3];
                    // transform location_x to fit image
                    location_x = location_x / this.imageMain.Source.Width * this.imageMain.ActualWidth;
                    double location_y = (double)current_item["points"][i * 3 + 1];
                    // transform location_y to fit image
                    location_y = location_y / this.imageMain.Source.Height * this.imageMain.ActualHeight;

                    Canvas.SetTop(this.kpoints[i], location_y - this.kpoints[i].Height);
                    Canvas.SetLeft(this.kpoints[i], location_x - this.kpoints[i].Width);
                    this.kpoints[i].PreviewMouseDown += kpoint_PreviewMouseDown;
                    CanvasMain.Children.Add(this.kpoints[i]);
                    
                    // create textblock
                    this.textBlocks[i] = new TextBlock();
                    this.textBlocks[i].Text = (i + 1).ToString();
                    this.textBlocks[i].Foreground = Brushes.LightGreen;
                    //bold 
                    this.textBlocks[i].FontWeight = FontWeights.Bold;
                    this.textBlocks[i].FontSize = 16;
                    Canvas.SetTop(this.textBlocks[i], Canvas.GetTop(this.kpoints[i]));
                    Canvas.SetLeft(this.textBlocks[i], Canvas.GetLeft(this.kpoints[i]) + this.kpoints[i].Width);
                    CanvasMain.Children.Add(this.textBlocks[i]);
                    // pair text with kpoint
                    this.textBlocks[i].Tag = this.kpoints[i];
                    this.kpoints[i].Tag = this.textBlocks[i];
                }
            }
            catch(Exception ex) {
                System.Windows.Forms.MessageBox.Show("Invalid Path: " + ex.Message);
            }

        }


        private void ButtonNext_Click(object sender, RoutedEventArgs e)
        {

            this.current_index = this.current_index + 1;
            if (this.current_index >= this.all_filepath.Count)
            {
                this.current_index = 0;
            }
            this.fn = System.IO.Path.GetFileName(this.all_filepath[this.current_index]);
            this.ButtonReload_Click(sender, e);

            // update kpoints, keep/discard button, and textblocks
            JObject current_item = (JObject)annotation[this.current_index];
            UpdateStatus();
            // parse current item to get all points
            for (int i = 0; i < 13; i++)
            {
                double location_x = (double)current_item["points"][i * 3];
                // transform location_x to fit image
                location_x = location_x / this.imageMain.Source.Width * this.imageMain.ActualWidth;
                double location_y = (double)current_item["points"][i * 3 + 1];
                // transform location_y to fit image
                location_y = location_y / this.imageMain.Source.Height * this.imageMain.ActualHeight;

                Canvas.SetTop(this.kpoints[i], location_y - this.kpoints[i].Height);
                Canvas.SetLeft(this.kpoints[i], location_x - this.kpoints[i].Width);

                // create textblock
                Canvas.SetTop(this.textBlocks[i], Canvas.GetTop(this.kpoints[i]));
                Canvas.SetLeft(this.textBlocks[i], Canvas.GetLeft(this.kpoints[i]) + this.kpoints[i].Width);

            }
        }

        private void ButtonPrev_Click(object sender, RoutedEventArgs e)
        {
            this.current_index = this.current_index - 1;
            if (this.current_index < 0)
            {
                this.current_index = this.all_filepath.Count - 1;
            }
            this.fn = System.IO.Path.GetFileName(this.all_filepath[this.current_index]);
            this.ButtonReload_Click(sender, e);
            // update kpoints, keep/discard button, and textblocks
            JObject current_item = (JObject)annotation[current_index];
            UpdateStatus();
            // parse current item to get all points
            for (int i = 0; i < 13; i++)
            {
                double location_x = (double)current_item["points"][i * 3];
                // transform location_x to fit image
                location_x = location_x / this.imageMain.Source.Width * this.imageMain.ActualWidth;
                double location_y = (double)current_item["points"][i * 3 + 1];
                // transform location_y to fit image
                location_y = location_y / this.imageMain.Source.Height * this.imageMain.ActualHeight;

                Canvas.SetTop(this.kpoints[i], location_y - this.kpoints[i].Height);
                Canvas.SetLeft(this.kpoints[i], location_x - this.kpoints[i].Width);

                // create textblock
                Canvas.SetTop(this.textBlocks[i], Canvas.GetTop(this.kpoints[i]));
                Canvas.SetLeft(this.textBlocks[i], Canvas.GetLeft(this.kpoints[i]) + this.kpoints[i].Width);

            }
        }

        private void ButtonSave_Click(object sender, RoutedEventArgs e)
        {
            //loops through annotation and removes all elements and images which have their id's status set to discard 
            for (int i = annotation.Count-1; i >=0; i--)
            {
                JObject current_item = (JObject)annotation[i];
                String path = System.IO.Path.Combine(this.currentImagePath, current_item["id"].ToString() + ".jpg");
                path.TrimEnd('\r', '\n');
                if (!(this.all_filepath[this.current_index].Equals(path)) && Keep_or_Discard[current_item["id"].ToString()].Equals("Discard"))
                {
                    System.GC.Collect();
                    System.GC.WaitForPendingFinalizers();
                    File.Delete(path);
                    annotation.Remove(annotation[i]);
                }
;
            }
            try
            {
               
                //string jsonObject = File.ReadAllText(this.annotationfn);


                System.Windows.Forms.SaveFileDialog saveDialog = new System.Windows.Forms.SaveFileDialog();


                if (saveDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    File.WriteAllText(saveDialog.FileName, annotation.ToString());
                }
            }
            catch (Exception ex)
            {
                System.Windows.Forms.MessageBox.Show("Something went wrong while saving:" +  ex.Message);
            }
            
        }

        private void Keep_or_Discard_Click(object sender, RoutedEventArgs e)
        {
            if (start)
            {
                JObject current = (JObject)annotation[current_index];
                if (Keep_or_Discard[current["id"].ToString()].Equals("Keep"))
                {
                    Keep_or_Discard[current["id"].ToString()] = "Discard";
                }
                else
                {
                    Keep_or_Discard[current["id"].ToString()] = "Keep";
                }
                UpdateStatus();
            }
        }
    }
    


}
