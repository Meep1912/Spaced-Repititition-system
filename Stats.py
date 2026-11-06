import Data
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
import datetime
import customtkinter as ctk




def Open_stat_view(mainwindow):


        # window config (Scrollable)
        root = ctk.CTkToplevel(mainwindow)
        root.title("Statistics")
        height_ = 500
        width_ = 600
        root.geometry(str(height_) + "x" + str(width_))
        stat_view_scrollable = ctk.CTkScrollableFrame(root, width=width_-50,height=height_-50)
        stat_view_scrollable.pack(fill="both", expand=True, padx=10,pady=10)

        # focus window
        root.after(100, root.focus)

        # fetch data
        stats = Data.get_file_data("stats")
        schedule = Data.get_file_data("schedule")


        month_timeframe_btn = 0
        year_timeframe_btn = 0
        alltime_timeframe_btn = 0

        # ------------- CHANGE THE TIME FRAME ----------------------

        def timeframe_changed():
        
            values = {
                0:"Month",
                1:"Year",
                2:"All Time",}
            
            timeframe = values[timeframe_scale.get()]
            timeframe_lbl.config(text=timeframe)

            # redraw graphs

            reviews_per_day(stats,timeframe)


        timeframe_scale = Scale(stat_view_scrollable, 
                                from_=0, 
                                to=2, 
                                orient="horizontal",
                                command=timeframe_changed)
        timeframe_scale.pack(padx=5, pady=5)
        
        timeframe_lbl= Label(stat_view_scrollable, text="0")
        timeframe_lbl.pack(padx=2, pady=2)

        # ------------- CHANGE THE TIME FRAME END -------------


        
        # graph of reviews per day
        def reviews_per_day(stats,timeframe):

            
            today = datetime.date.today()

            timeframes = {"Month":30,
                          "Year":365,
                          "All Time":None}

            days = timeframes[timeframe]

            reviews_per_day = {day: sum(len(r) for r in cards.values())
             for day, cards in stats.items()}

            # All Time

            if days is None:  
                first = min(map(datetime.date.fromisoformat, reviews_per_day), default=today)
                days = (today - first).days + 1

            # Month and year
            dates = [today - datetime.timedelta(days=i)
            for i in range(days - 1, -1, -1)]
            counts = [reviews_per_day.get(d.isoformat(), 0) for d in dates]



            # make data:

            def draw_graph(x,y):
                # plot
                fig, ax = plt.subplots()

                ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)
                ax.set_title("Reviews per day")
                fig.autofmt_xdate()
                canvas = FigureCanvasTkAgg(fig, master=stat_view_scrollable)  # A tk.DrawingArea.
                canvas.draw()
                canvas.get_tk_widget().pack(side=TOP,expand=True, fill="x")

                # loop through days selected in preset

            draw_graph(dates,counts)
        # pi chart of what cards are new, learning, mature, suspended

        def card_states_pichart(schedule,timeframe):

            def find_states(schedule):
                # find new, learning, young, mature suspended amounts
                new = 0
                learning = 0
                relearning = 0
                young = 0
                mature = 0
                suspended = 0

                for card in schedule.keys():
                    interval = schedule[card]["Interval"]

                    if schedule[card]["Suspended"] == True:
                        suspended += 1
                    else:
                        if schedule[card]["Due"] == "0":
                                isnew = True
                        else:
                                isnew = False  

                        if interval == 0:
                                if isnew:
                                    new += 1
                                else:
                                    relearning +=1
                                # check relearning stat

                        learning_steps = [1,3]

                        if interval in learning_steps:
                            if isnew:
                                relearning += 1
                            else:
                                learning += 1

                        mature_paramater = 20

                        if interval > learning_steps[len(learning_steps)-1]:
                            if interval < mature_paramater:
                                young += 1
                            else:
                                mature += 1

                values = {"new":new,
                    "learning":learning,
                    "relearning":relearning,
                    "young":young,
                    "mature":mature,
                    "suspended":suspended}

                values2 = dict(values)

                counter = 0
                for value in values2.keys():
                     if values[value] == 0:
                        values.pop(value)
                        counter += 1


                x = [new,learning,relearning,young,mature,suspended]

                for i in range(0,counter):
                    x.remove(0)

                return values,x

            values, x = find_states(schedule)

                     
            colors = plt.get_cmap('Greens')(np.linspace(0.2, 0.7, len(x)))

            # plot
            fig, ax = plt.subplots()

            labels_list = []

            for label in values.keys():
                    labels_list.append(label + " "+ str(values[label]))

            hatches = ["O","/","X","//","..","xx"]

            ax.pie(x, labels=labels_list, colors=colors, radius=3, center=(4, 4),
                   hatch=hatches, pctdistance=1.25, labeldistance=.6,
                   wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)

            ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
                   ylim=(0, 8), yticks=np.arange(1, 8))

            card_states_pichart_canvas = FigureCanvasTkAgg(fig, master=stat_view_scrollable)  # A tk.DrawingArea.
            card_states_pichart_canvas.draw()
            card_states_pichart_canvas.get_tk_widget().pack(side=TOP,expand=True, fill="x")

        timeframe = "Month"
        reviews_per_day(stats, timeframe)
        card_states_pichart(schedule, timeframe)

