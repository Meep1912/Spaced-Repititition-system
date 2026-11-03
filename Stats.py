import Data
from tkinter import *
#import matplotlib.pyplot as plt
#import numpy as np
#from matplotlib.backends.backend_tkagg import (
    #FigureCanvasTkAgg, NavigationToolbar2Tk)





def Open_stat_view():
        return 0
        stat_frame = Tk()
        stat_frame.title("Statistics")
        stat_frame.geometry("900x600")

        stats = Data.get_file_data("stats")
        schedule = Data.get_file_data("schedule")


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
        def reviews_per_day(stats):
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
            y = []
            for day in review_per_day:
                if day > longest:
                    longest = day

                y.append(1.2 * longest)

            x = review_per_day

            # plot
            fig, ax = plt.subplots()

            ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)

            # https://matplotlib.org/3.1.0/api/backend_tkagg_api.html#module-matplotlib.backends.backend_tkagg
            # use this link to connect the graph to tkinter

            canvas = FigureCanvasTkAgg(fig, master=stat_frame)  # A tk.DrawingArea.
            canvas.draw()
            canvas.get_tk_widget().pack(side=TOP)

            # loop through days selected in preset

        # pi chart of what cards are new, learning, mature, suspended

        def card_states_pichart(schedule):

            # find new, learning, mature and suspended
            new
            learning
            relearning
            mature
            suspended
            for card in schedule.keys():
                interval = schedule[card]["Interval"]
                if schedule[card]["Due"] == "0"
                        isnew = True
                else:
                        isnew = False
                        
                if interval == 0
                        if isnew:
                                new += 1
                        else:
                                relearning +=1
                        # check relearning stat
                elif interval =
        

            x = [1, 2, 3, 4, 5]

            colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))

            # plot
            fig, ax = plt.subplots()

            ax.pie(x, colors=colors, radius=3, center=(4, 4),
                   wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)

            ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
                   ylim=(0, 8), yticks=np.arange(1, 8))

            card_states_pichart_canvas = FigureCanvasTkAgg(fig, master=stat_frame)  # A tk.DrawingArea.
            card_states_pichart_canvas.draw()
            card_states_pichart_canvas.get_tk_widget().pack(side=TOP)

        reviews_per_day(stats)
        card_states_pichart(schedule)
