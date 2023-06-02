# streamlit_data_vis
NYC_Crash_Visualization

Data was initially loaded from https://catalog.data.gov/dataset/motor-vehicle-collisions-crashes and cleaned using the code below in order to reduce the file size

Loading all the libraries
import datetime
import pandas as pd


# Loading data which was sourced from https://catalog.data.gov/dataset/motor-vehicle-collisions-crashes

# In[2]:


df = pd.read_csv('/Users/Andrew/Desktop/Practicum/Sprint 4 - Software Development Tools/Project Data/vehicle_crashes.csv', low_memory=False)


# Dropping columns that will not be used in order to make file size smaller

# In[3]:


df = df.drop(columns=['BOROUGH', 'LATITUDE', 'LONGITUDE', 'LOCATION', 
                      'ON STREET NAME', 'CROSS STREET NAME', 'OFF STREET NAME', 'NUMBER OF PEDESTRIANS INJURED',
                     'NUMBER OF PEDESTRIANS KILLED', 'NUMBER OF CYCLIST INJURED', 'NUMBER OF CYCLIST KILLED',
                     'NUMBER OF MOTORIST INJURED', 'NUMBER OF MOTORIST KILLED', 'COLLISION_ID', 'CONTRIBUTING FACTOR VEHICLE 3',
                     'CONTRIBUTING FACTOR VEHICLE 4', 'CONTRIBUTING FACTOR VEHICLE 5', 'VEHICLE TYPE CODE 3', 'VEHICLE TYPE CODE 4',
                     'VEHICLE TYPE CODE 5'])


# Renaming columns with better names

# In[4]:


df.columns = ['date', 'time', 'zip_code', 'number_injured', 'number_killed', 
              'factor_vehicle_1', 'factor_vehicle_2', 'vehicle_1_type', 'vehicle_2_type']


# Changing appropriate columns to datetime type 

# In[5]:


df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')


# In[6]:


df['time'] = pd.to_datetime(df['time'], format='%H:%M')


# Filling na values with 'unspecified' for vehicle 1 and 'N/A' for vehicle 2. 

# In[7]:


df['factor_vehicle_1'] = df['factor_vehicle_1'].fillna('unspecified')
df['factor_vehicle_2'] = df['factor_vehicle_2'].fillna('N/A')


# Filling na values for injured and killed to 0 

# In[8]:


df['number_injured'] = df['number_injured'].fillna(0)


# In[9]:


df['number_killed'] = df['number_killed'].fillna(0)


# Coverting factors to lowercase and correcting data types that are unspecified

# In[10]:


df['factor_vehicle_1'] = df['factor_vehicle_1'].str.lower()
df['factor_vehicle_2'] = df['factor_vehicle_2'].str.lower()


# In[11]:


df['factor_vehicle_1'] = df['factor_vehicle_1'].where(df['factor_vehicle_1'] != 'illnes', 'illness')
df['factor_vehicle_2'] = df['factor_vehicle_2'].where(df['factor_vehicle_2'] != 'illnes', 'illness')


# In[12]:


df['factor_vehicle_1'] = df['factor_vehicle_1'].where(df['factor_vehicle_1'] != '1', 'unspecified')
df['factor_vehicle_2'] = df['factor_vehicle_2'].where(df['factor_vehicle_2'] != '1', 'unspecified')


# In[13]:


df['factor_vehicle_1'] = df['factor_vehicle_1'].where(df['factor_vehicle_1'] != '80', 'unspecified')
df['factor_vehicle_2'] = df['factor_vehicle_2'].where(df['factor_vehicle_2'] != '80', 'unspecified')


# Checking uniqe factors 

# In[14]:


factors = df['factor_vehicle_1'].unique()


# In[15]:


sorted(factors)


# Checking df characteristics. File size still too large. Dropping all remaining na values to reduce file size. 

# In[16]:


df.info(show_counts=True)


# In[17]:


df = df.dropna()


# In[18]:


df.info(show_counts=True)


# Removing all data before 1/1/2015 to further reduce file size. 

# In[19]:


df = df[df['date'] >= '01/01/2015']


# Exporting df to csv to be used as primary file moving forward 

# In[20]:


df.to_csv('/Users/Andrew/Desktop/Practicum/Sprint 4 - Software Development Tools/Project Data/vehicle_crashes_cleaned.csv', index=False)


# In[21]:


#df_factor = df.groupby(['factor_vehicle_1'])['factor_vehicle_1'].count().sort_values(ascending=False)


# In[22]:


#df_factor