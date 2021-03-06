#!/usr/bin/env python

import os
import datetime
import tkinter as tk
from tkinter import filedialog

import piexif
import plotly
import plotly.graph_objs as go

pwd = 'test-images/'


def get_timestamps(dir, recursive=False):
    timestamp_list = []
    if recursive: # still has a bug (subdirs are not added to filename)
        file_list = []
        for root, dirs, files in os.walk(dir):
            file_list.extend(files)
    else:
        file_list = os.listdir(dir)
    for filename in file_list:
        try:
            datetimestr = piexif.load(dir + '/' + filename)['Exif'][36867].decode("utf-8")
            timestamp = datetime.datetime.strptime(datetimestr, '%Y:%m:%d %H:%M:%S')
            timestamp_list.append(timestamp)
        except:
            continue
    return timestamp_list


def create_scatter(timestamps):
    timestamps_scatter = go.Scatter(
        x=timestamps,
        y=[0 for i in timestamps],
        name='timestamps',
        hoverinfo='x',
        hoveron='points',
        mode='markers',
        marker={
            'symbol': 'circle',
            'opacity': 1,
            'size': 9,
            'color': '#1f77b4',
            'line': {
                'color': '#444',
                'width': 0
            },
            'gradient': {
                'type': None
            },
            'maxdisplayed': 0
        }
    )
    return timestamps_scatter


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('Image Punch Chart')
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        self.select_dir_button = tk.Button(self, text="Select image directory", command=self.get_path, width=25)
        self.select_dir_button.pack()

    @property
    def create_layout(self):
        layout = go.Layout(
            showlegend=False,
            xaxis={
                'showgrid': False,
                'fixedrange': False
            },
            yaxis={
                'showgrid': False,
                'showticklabels': False,
                'rangemode': 'normal',
                'range': [-.1, .1],
                'fixedrange': True
            },
            hovermode='closest'
        )
        return layout

    def get_path(self):
        try:
            with open('last_path', 'r') as f:
                initial_dir = f.read()
        except:
            print('no last path stored')
            initial_dir = '~/'
        path = filedialog.askdirectory(
            title="Select image directory",
            initialdir=initial_dir
        )

        if path:
            try:
                with open('last_path', 'w') as f:
                    f.write(path)
                timestamps = get_timestamps(path)
                fig = go.Figure(data=[create_scatter(timestamps)], layout=self.create_layout)
                punch_chart = plotly.offline.plot(fig, filename='punch-chart.html', auto_open=True)
            except:
                pass


root = tk.Tk()
app = Application(master=root)
app.update_idletasks()
app.mainloop()
