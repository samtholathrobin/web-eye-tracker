from screeninfo import get_monitors
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

class EyeInfo:
    def __init__(self,  calib_points=[], dataset='./data.csv', screen_width=0, screen_height=0,  is_right = False, is_left = False,):
            self.is_right = is_right
            self.is_left = is_left
            self.dataset = dataset

            self.right_eye_df = None
            self.left_eye_df = None
            self.prediction_df = None

            self.calib_points = calib_points
            self.calib_df = None


            self.screen_width = screen_width
            self.screen_height = screen_height

            self.palette = {
                'calib_df': 'black',
                'first': 'blue',
                'second': 'red',
                'third': 'green',
                'fourth': 'yellow',
                'fifth':'lightgreen'
            }

            self.legend_dict = {
                self.palette['first']: 'Cluster 1',
                self.palette['second']: 'Cluster 2',
                self.palette['third']: 'Cluster 3',
                self.palette['fourth']: 'Cluster 4',
                self.palette['fifth']: 'Cluster 5',
            }

    def init_eye(self):
        self.init_screen_resolution()
        self.init_calib_points()
        self.init_points()
        

    def init_screen_resolution(self):
        monitors = get_monitors()
        if monitors:
            primary_monitor = monitors[0]
            self.screen_width = primary_monitor.width 
            self.screen_height = primary_monitor.height
        else:
            self.screen_width = self.screen_width
            self.screen_height = self.screen_height

    def init_calib_points(self):
        if self.calib_points:
            post_calib = []
            for point in self.calib_points:
                calibrated_point = {
                    "screen_x": point["x"],
                    "screen_y": point["y"],
                    "order":    point["order"]
                }
                post_calib.append(calibrated_point)
            df = pd.DataFrame(post_calib)
            self.calib_df = df

    def init_points(self):
        try:
            data = pd.read_csv(self.dataset)
            if self.is_right:
                self.prediction_df = data[['screen_x', 'screen_y','right_iris_x', 'right_iris_y']]
            elif self.is_left:
                self.prediction_df = data[['screen_x', 'screen_y','left_iris_x', 'left_iris_y']]
            else:
                self.prediction_df = data[['screen_x', 'screen_y','right_iris_x', 'right_iris_y','left_iris_x', 'left_iris_y']]

        except FileNotFoundError:
            print(f"File {self.dataset} not found.")
        except Exception as e:
            print(f"An error occurred while reading the CSV file: {str(e)}")
    
    def plot(self, dataset, key_x, key_y, is_subset, subset_size, lock_plot):
        sns.set(style="whitegrid")
        sns.scatterplot(data=self.calib_df, x=f'{key_x}', y=f'{key_y}',size='order', color=self.palette['calib_df'])
        if is_subset:
            subset_df1r = dataset.iloc[0:subset_size]
            subset_df2r = dataset.iloc[subset_size:subset_size*2]
            subset_df3r = dataset.iloc[subset_size*2:subset_size*3]
            subset_df4r = dataset.iloc[subset_size*3:subset_size*4]
            subset_df5r = dataset.iloc[subset_size*4:subset_size*5]
            
            sns.scatterplot(data=subset_df1r, x=f'{key_x}', y=f'{key_y}', color=self.palette['first'])
            sns.scatterplot(data=subset_df2r, x=f'{key_x}', y=f'{key_y}', color=self.palette['second'])
            sns.scatterplot(data=subset_df3r, x=f'{key_x}', y=f'{key_y}', color=self.palette['third'])
            sns.scatterplot(data=subset_df4r, x=f'{key_x}', y=f'{key_y}', color=self.palette['fourth'])
            sns.scatterplot(data=subset_df5r, x=f'{key_x}', y=f'{key_y}', color=self.palette['fifth'])
            for color, label in self.legend_dict.items():
                plt.scatter([], [], c=color, label=label)
            plt.legend()
        else:
            sns.scatterplot(data=dataset, x=f'{key_x}', y=f'{key_y}', color=self.palette['first'])
        
        plt.xlabel('')
        plt.ylabel('')
        if lock_plot:
            plt.xlim(0, self.screen_width)
            plt.ylim(0, self.screen_height)
        plt.show()