import Data
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np






def Open_stat_view():

        stat_frame = Tk()
        stat_frame.title("Statistics")
        stat_frame.geometry("500x400")

        # ---------------- Temp --------------------

        Data.load_files_startup()
        
        # ---------------- Temp --------------------
        stats = Data.get_file_data("stats")

        month_timeframe_btn = 0
        year_timeframe_btn = 0
        alltime_timeframe_btn = 0

        # ------------- CHANGE THE TIME FRAME ----------------------

        def timeframe_changed(event):
            values = {
                0:"Month",
                1:"Year",
                2:"All Time",}
            
            
            timeframe_lbl.config(text=values[event.widget.get()])

        timeframe_scale = Scale(stat_frame, from_=0, to=2, orient="horizontal")
        timeframe_scale.bind("<Motion>", timeframe_changed)
        timeframe_scale.pack(padx=5, pady=5)
        
        timeframe_lbl= Label(stat_frame, text="0")
        timeframe_lbl.pack(padx=2, pady=2)

        # ------------- CHANGE THE TIME FRAME END -------------


        
        # graph of reviews per day


        review_per_day = []
        for day in stats.keys():
            for card in stats[day]:
                days_reviews = len(stats[day][card])
                review_per_day.append(days_reviews)

        

        plt.style.use('_mpl-gallery')

        # make data:
        x = 0.5 + np.arange(8)

        # find the highest reviews in the set

        longest = 0
        for day in review_per_day:
            if day > longest:
                longest = day
                
        y = 1.2 * longest
        x = review_per_day

        # plot
        fig, ax = plt.subplots()

        ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)

        ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
               ylim=(0, 8), yticks=np.arange(1, 8))

        plt.show()

        # https://matplotlib.org/3.1.0/api/backend_tkagg_api.html#module-matplotlib.backends.backend_tkagg
        # use this link to connect the graph to tkinter
                

        # loop through days selected in preset
Open_stat_view()
