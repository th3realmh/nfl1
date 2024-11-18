#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# Questions Answered:
# - Which states have the highest fall 2022 enrollment?- 	Which institutions have the highest fall 2022 enrollment
# 
# 
# Assumptions:
# - UNITID = a unique college (indiscriminant of campus)
# - One unique enrollment count per college (indiscriminant of campus)
# - Campus and college are interchangeable
# - All N/As are 0s?
# 

# #### Methodology: 
# Merge the 2022 data set state and college name metadata (college_and_state_names_df) into the Fall Enrollment Dataset (fall_enrollment_df), joined by UNITID to add the state and college name to the Fall Enrollment Dataframe.

# In[2]:


college_df = pd.read_csv('Downloads/EFFY2022.csv') #Aggregate college data for all of 2022
college_dict_df = pd.read_excel('Downloads/EFFY2022dict.xlsx', sheet_name = 'varlist') #changes names in data aggregate college data
college_and_state_names_df = pd.read_csv('Downloads/ic2022_campuses_data_stata.csv', encoding='latin-1') #university and state, merge on unitid


# In[3]:


fall_college_df = pd.read_csv('Downloads/ef2022a.csv') #(e2022a)
fall_enrollment_df = pd.read_csv('Downloads/ef2022d.csv') #[[UNITID, UGENTERN (enrollment)]]


# Reduce Dataframes to their valuable subsets, including UNITID for merging, enrollment, State and Institution

# In[4]:


fall_enrollment_df = fall_enrollment_df[['UNITID', 'UGENTERN']] #id, 2022 fall enrollment
college_and_state_names_df = college_and_state_names_df[['UNITID','PCINSTNM','PCSTABBR']] #id, institution name and state


# Set UNITID to string type; Merge Enrollment With State via UNITID

# In[5]:


fall_enrollment_df['UNITID'] = fall_enrollment_df['UNITID'].astype(str)
college_and_state_names_df['UNITID'] = college_and_state_names_df['UNITID'].astype(str)


# In[6]:


fall_enrollment_df = fall_enrollment_df.merge(college_and_state_names_df, on='UNITID')


# In[7]:


#clean fall_enrollment_df
fall_enrollment_df = fall_enrollment_df.dropna()
fall_enrollment_df = fall_enrollment_df.drop_duplicates(subset=['UNITID'])


# In[8]:


fall_enrollment_df.rename(columns={'UGENTERN': 'Enrollment', 'PCSTABBR': 'State', 'PCINSTNM': 'Campus'}, inplace=True)


# In[9]:


fall_enrollment_df = fall_enrollment_df.set_index('UNITID')


# In[10]:


highest_enrollment_df = fall_enrollment_df.sort_values(by=['Enrollment'], ascending = False).head(10)
highest_enrollment_df


# In[11]:


highest_enrollment_df.index[0]


# In[12]:


f"{highest_enrollment_df['Campus'][0]}, UNITID {highest_enrollment_df.index[0]}, is the college with the highest fall enrollment."


# In[13]:


state_enrollment_df = fall_enrollment_df.groupby('State')['Enrollment'].sum().reset_index().sort_values(['Enrollment'], ascending=False).head(10)
state_enrollment_df


# In[14]:


f"{state_enrollment_df['State'].iloc[0]} is the state with the highest fall enrollment."


# Potential Improvements:
# 
# - Data Visualization to show different enrollment in the top 10 states via violin plots
# - More data inputted the IDEPS
# - Include diversity data, public and private institution data

# ## Appendix:
# ### Spring and fall of 2022 (Background analysis)

# In[4]:


college_and_state_names_df.nunique()


# In[5]:


college_df.shape


# In[6]:


agg_college_df = college_df.groupby('UNITID').sum()


# In[7]:


agg_college_df.columns.shape


# In[8]:


college_dict_df['varTitle'].shape


# In[9]:


agg_college_df.head(2)


# In[10]:


old_columns_list = agg_college_df.columns
new_columns = dict(zip(college_dict_df['varname'], college_dict_df['varTitle']))
agg_college_df = agg_college_df.rename(index=str, columns=new_columns)


# In[11]:


agg_college_df = agg_college_df.drop(columns=old_columns_list, errors = 'ignore')


# In[12]:


#[agg_college_df.pop(x) for x in old_columns_list, errors = 'ignore']


# In[13]:


agg_college_df.shape


# In[14]:


agg_college_df = agg_college_df.reset_index()


# In[15]:


agg_college_df


# In[16]:


agg_college_df['UNITID'] = agg_college_df['UNITID'].astype(str)
college_and_state_names_df['UNITID'] = college_and_state_names_df['UNITID'].astype(str)


# In[17]:


#agg_college_df.merge(college_and_state_names_df.dropna(subset=['UNITID','PCINSTNM','PCSTABBR']), on='UNITID')


# In[18]:


agg_college_df.merge(college_and_state_names_df[['UNITID','PCINSTNM','PCSTABBR']], on='UNITID')


# In[19]:


college_and_state_names_df.columns


# In[ ]:




