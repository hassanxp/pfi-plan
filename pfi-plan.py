#!/usr/bin/env python
# coding: utf-8

# In[1]:


import plotly.figure_factory as ff
import pandas as pd
import random
import plotly.graph_objects as go


# In[13]:


catColors = dict(Project='rgb(255, 51, 0)', 
                 Hardware='rgb(230, 230, 0)', 
                 CobraOperation='rgb(51, 153, 255)', 
                 CobraDataAnalysis='rgb(102, 0, 255)', 
                 FiberConfiguration='rgb(153, 102, 255)', 
                 Calibration='rgb(204, 51, 255)',
                 Infra='rgb(153, 0, 153)')


# In[14]:


def plt_line(df, fig, mls_yr, mls_text, color="gray"):
    
    fig.add_trace(
        go.Scatter(
            x = [mls_yr, mls_yr],
            y = [-1, len(df.index) + 1],
#            mode = "lines",
            mode = "lines+text",
            name = mls_text,
            textposition = "bottom center",
            line = go.scatter.Line(color = color, width = 1),
            showlegend = False
        )
    )


# In[15]:


def plot_plan(plan_file):
    # Load in CSV
    df0 = pd.read_csv(plan_file, skipinitialspace=True,  quotechar='"').applymap(lambda x: x.strip() if type(x)==str else x).iloc[::-1]

    # Filter out columns not needed for gantt plot
    df = df0[['Task', 'Start', 'Finish', 'Complete', 'Category']].copy()

    for cat in set(df['Category']):
        if cat not in catColors:
            print(f'category {cat} is not in color mapping') 

    arms_full = df[df['Task'] == 'SM3(B+R+N)@LAM']['Start'].values[0]
    engobs_start = df[df['Task'] == 'Engineering observations']['Start'].values[0]
    engobs_end = df[df['Task'] ==  'Engineering observations']['Finish'].values[0]
    ssp_end = df[df['Task'] == 'Call for SSP']['Start'].values[0]

    fig = ff.create_gantt(df, colors=catColors, index_col='Category',
                          show_colorbar=False, 
                          bar_width=0.1, 
                          showgrid_x=True, 
                          showgrid_y=False, 
                          title=plan_file,
                          height=1500,
                          width=2000)
    fig.update_layout(plot_bgcolor='rgba(0,0,0, 0.1)')

    plt_line(df, fig, '2021-08-31', 'MSIP End', color='red')
    plt_line(df, fig, arms_full, 'R+B+N', color='gray')
    plt_line(df, fig, engobs_start, 'Eng Obs Start', color='green')
    plt_line(df, fig, ssp_end, 'Call for SSP', color='black')
    plt_line(df, fig, engobs_end , 'Eng Obs End', color='green')

    fig.show(renderer='browser')


# In[17]:


plot_plan('pfi-plan.csv')


# In[ ]:




