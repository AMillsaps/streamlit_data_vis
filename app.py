#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('pip', 'install streamlit')
import datetime
import pandas as pd
import plotly.express as px
import streamlit as st


# In[2]:


df = pd.read_csv('vehicle_crashes_cleaned.csv', low_memory=False)


# In[3]:


df.tail()


# In[4]:


df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')


# In[5]:


df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')


# In[6]:


df.info()


# In[7]:


def hr_func(ts):
    return ts.hour


# In[8]:


df['hour'] = df['time'].apply(hr_func)


# In[9]:


df['injured+killed'] = df['number_injured'] + df['number_killed']


# In[10]:


df.info()


# In[11]:


df.plot(kind='scatter', figsize=[9, 6], x='hour', y='injured+killed', 
                          title="People Injured or Killed By Hour", xlabel='Time of Day', ylabel='People Injured or Killed')


# In[12]:


df['zip_code'] = pd.to_numeric(df['zip_code'], errors='coerce')


# In[13]:


df['zip_code'].plot(kind='hist', figsize=[9, 6], x='zip_code', bins=50, 
                          title="Frequency of Accidents By Zip Code", xlabel='Zipcode')


# In[14]:


df['number_injured'].plot(kind='hist', figsize=[9, 6], x='number_injured', bins=25, 
                          title="Frequency of Number of People Injured in Accident")


# In[15]:


injured_or_killed_only = df[(df['number_injured'] > 0) | (df['number_killed'] > 0)]


# In[16]:


injured_or_killed_only


# In[25]:


st.header('Characteristics of Accidents with Injuries or Death')
st.write("""
#### Filter the data below to see the ?? by Crash Factor""")
inclulde_unspecified_factors = st. checkbox('Include crashes with unspecified factors for vehicle 1')


# In[26]:


inclulde_unspecified_factors


# In[27]:


if not inclulde_unspecified_factors:
    injured_or_killed_only = injured_or_killed_only[injured_or_killed_only.factor_vehicle_1!='unspecified']


# In[28]:


factor_choice = injured_or_killed_only['factor_vehicle_1'].unique()
make_choice_factor = st.selectbox('Select factor:', factor_choice)


# In[31]:


make_choice_factor


# In[33]:


#creating hours as sliders
min_hour, max_hour = int(injured_or_killed_only['hour'].min()), int(injured_or_killed_only['hour'].max())

#creating slider
hour_range = st.slider("Choose hours", value=(min_hour,max_hour), min_value=min_hour, max_value=max_hour)


# In[34]:


hour_range


# In[35]:


#filtering dataset on chosen factor vehicle 1 and chosen year range
filtered_type = injured_or_killed_only[(injured_or_killed_only.factor_vehicle_1==make_choice_factor) & 
                                       (injured_or_killed_only.hour >= hour_range[0]) & 
                                       (injured_or_killed_only.hour <= hour_range[1])]
#showing the final table on streamlit
st.table(filtered_type)


# In[36]:


filtered_type


# In[37]:


st.header('Injury and/or Death Analysis')
st.write("""
#### Let's analyze what influences injury and/or death the most. We will check how distribution of injury or death
varies depending on vehicle 1 type, vehicle 2 type, factor for vehicle 1, and factor for vehicle 2""")

#create histogram with parameter of choice: vehicle 1 type, vehicle 2 type, factor for vehicle 1, factor, for vehicle 2

#creating list of options to choose from 
list_for_hist = ['vehicle_1_type', 'vehicle_2_type', 'factor_vehicle_1', 'factor_vehicle_2']

#creating selectbox
choice_for_hist = st.selectbox('Split for injured or killed distribution', list_for_hist)

#plotly histogram, where injured+killed is split by the choice made in the selectbox
fig1 = px.histogram(injured_or_killed_only, x="injured+killed", color=choice_for_hist)

#adding title
fig1.update_layout(title="<b> Split of injured or killed by {}<b>".format(choice_for_hist))

#embedding into streamlit
st.plotly_chart(fig1)


# In[38]:


fig1.show()


# In[42]:


#creating time of day category to use to analyze the number injured and/or killed
def time_category(x):
    if x<6: return 'Early Morning'
    elif x>= 6 and x<12: return 'Morning'
    elif x>= 12 and x<16: return 'Afternoon'
    elif x>16 and x<20: return 'Evening'
    else: return 'Night'
    
df['time_category'] = df['hour'].apply(time_category)


# In[43]:


df['time_category']


# In[45]:


def month_func(ts):
    return ts.month


# In[46]:


df['month'] = df['date'].apply(month_func)


# In[48]:


st.write("""
#### Now let's check how the number of injured or killed is impacted by time of day or month""")

#distribution of accident count depending on time of day
list_for_scatter = ['hour', 'month']
choice_for_scatter = st.selectbox('Total accident count dependency on ', list_for_scatter)
fig2 = px.scatter(df, x=choice_for_scatter, y='injured+killed')

fig2.update_layout(title="<b> {} vs number injured or killed".format(choice_for_scatter))
st.plotly_chart(fig2)


# In[49]:


fig2


# In[ ]:


streamlit run eda.py


# In[ ]:





# In[17]:


injured_or_killed_only_grouped_by_factor_1 = injured_or_killed_only.groupby('factor_vehicle_1')['date'].count().reset_index()


# In[18]:


injured_or_killed_only_grouped_by_factor_1.columns=['factor_name', 'factor_1_count']


# In[19]:


injured_or_killed_only_grouped_by_factor_2 = injured_or_killed_only.groupby('factor_vehicle_2')['date'].count().reset_index()


# In[20]:


injured_or_killed_only_grouped_by_factor_2.columns=['factor_name', 'factor_2_count']


# In[21]:


inj_or_killed_combined = injured_or_killed_only_grouped_by_factor_1.merge(injured_or_killed_only_grouped_by_factor_2, on='factor_name', how='outer')


# In[22]:


inj_or_killed_combined['factor_2_count']=inj_or_killed_combined['factor_2_count'].fillna(0)


# In[23]:


inj_or_killed_combined['count_total'] = inj_or_killed_combined['factor_1_count'] + inj_or_killed_combined['factor_2_count']


# In[24]:


inj_or_killed_combined


# In[ ]:




