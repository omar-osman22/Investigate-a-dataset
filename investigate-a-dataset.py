#!/usr/bin/env python
# coding: utf-8

# 
# # Project: Investigate a Dataset (Replace this with something more specific!)
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# > What are the factors can affect your decision to show up for your medical appointment, what if you are far away from your 
# hospital can the Scholarship changes your mind? 
# 
# > This dataset collects informationfrom 100k medical appointments in Brazil and is focused on the question of whether or not patients show up for their appointment. A number of characteristics about the patient are included like: Gender, Age, Neighbourhood, Scholarship, SMS_received and more other detils.
# 
# > 

# In[1]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.
# Use this cell to set up import statements for all of the packages that you
#   plan to use.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
# Remember to include a 'magic word' so that your visualizations are plotted
#   inline with the notebook. See this page for more:
get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# 
# ### General Properties

# In[3]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.
# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.
df = pd.read_csv('medical_appointments.csv')
df.head()


# In[4]:


df.columns


# In[5]:


df.info()


# In[6]:


df.describe()


# ## NOTE
# Here, there is an obvious mistake as the minimum age is minus,,
# Max age : 115 years

# In[7]:


#The number of rows is equal to the total number of patients
df.shape


# 
# ### Data Cleaning (Replace this with more specific notes!)

# In[8]:


#Firstly I will drop the columns of PatientId and appointment day cause i will not use them in my analyis
df.drop(['PatientId','AppointmentID'], axis=1, inplace= True)
df.head()


# In[9]:


#I will delete the time and keep only the date in appointment day and scheduledday columns to get the difference between them 
#and see if the gap between the two dates affect the patient decision to come 

for col in ["AppointmentDay", "ScheduledDay"]:
    df[col] = df[col].apply(lambda x: x.split("T")[0])
    


# In[10]:


#As The type of appointment day and scheduled day is object i will convert it to date
for col in ["ScheduledDay", "AppointmentDay"]:
    df[col] = pd.to_datetime(df[col])


# In[12]:


# To be able to visualize how showed up for their appointment and who
# didn't, I will rename no_show column to Show and replace (No) by 1 
# and (Yes) by 0, then 1 means that the patient have come(No of No_Show) and 0 means he
# haven't come
df.rename(columns= {"No-show":"Show"}, inplace= True)
labels = {"No":1, "Yes":0}
df["Show"] = df["Show"].map(labels)
df["Show"] = df["Show"].astype(int)


# In[13]:


df.info()


# In[14]:


#Now, I will use rename method to change some columns names due to their miss spelling or to avoid any mess
df.rename(columns={'No-show':'No_Show','Hipertension':'Hypertension'}, inplace= True)


# In[15]:


#I Will drop the row of the patient having age with minus 
#firtly i will search for rows have age less than zero
df[df["Age"] < 0]


# In[16]:


#Then I will drop it
df.drop(99832, inplace= True)


# In[17]:


#Making Sure that it was removed
df[df["Age"] < 0]


# In[18]:


#Before Visualizing Data, I Will Drop Appointment Day and Scheduled Day Coulmns as i will nt use them, i only will need the
#delay column which i create from the difference between them 
df.drop(['ScheduledDay','AppointmentDay'], axis= 1, inplace= True)


# # Data Visualization 
# ### General Look on all Data
# #### I Will Use hist function to plot all varibles and try to get pattes

# In[19]:


df.hist(figsize= (30,20));


# ## The Data Visualiztion shows us that 
# Most of Patients are between 0 - 45 years old.
# 
# Most of patients are not enrolled in the scholarship.
# 
# Most of patients don't complain of chronic diseases (like: diabetes, hypertension, handcap)
# 
# Also there is a strange notice that most of patients who have come didn't recieve a message to remind them with their appointment

# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# ### Research Question 1 (Does The Scholrship affect patients attendance?)

# In[24]:


# Use this, and more code cells, to explore your data. Don't forget to add
#   Markdown cells to document your observations and findings.
scholar_effect = df.groupby('Scholarship')['Show'].count()
scholar_effect.plot(kind= 'bar', title= 'Relation between showing up and scholarship', alpha = 0.7);
plt.xlabel('Scholarship', fontsize= 14)
plt.ylabel('Show', fontsize= 14)


# ### Nearly 950000 patients had show up for their appointment and they are not enrolled in the scolarship
# 
#  It's clear that the Scholarship didn't affect the attenance of patients as a big number of who has come, had not have a scholarsip
# then Scholarship is not significant sign

# ### Research Question 2  (Does Recieving a message or not affects patients attendance?)

# In[25]:


# Continue to explore the data to address your additional research
#   questions. Add more headers as needed if you have more questions to
#   investigate.
scholar_effect = df.groupby('SMS_received')['Show'].count()
scholar_effect.plot(kind= 'bar', title= 'Relation between showing up and SMS Received', alpha = 0.7);
plt.xlabel('SMS Received', fontsize= 14)
plt.ylabel('Show', fontsize= 14)


# ### Nearly 70000 patients had show up for their appointment and they didn't recieve a reminding sms
#  It's clear that recieving sms didn't affect the attenance of patients as a big number of who has come, had not recieved a sms 
#  then sms recieving is not significant sign

# In[43]:


diabetes_effect = df.groupby('Diabetes')['Show'].count()
diabetes_effect.plot(kind= 'bar', title= 'Relation between showing up and Diabetes', alpha = 0.7);
plt.xlabel('Diabetes', fontsize= 14)
plt.ylabel('Show', fontsize= 14)


# ### Nearly 950000 patients had show up for their appointment and they don't complains of diabetes
#  It's also clear that daibetes didn't affect the attenance of patients as a big number of who has come, were not diabetics

# ### Research Question 3  (Does the patient's city  affects its attendance?)

# In[44]:


show = (df.Show == 1)
no_show = (df.Show == 0)


# In[45]:


df[show].count()


# In[46]:


df[no_show].count()


# In[51]:


plt.figure(figsize=[12,8])
df.Neighbourhood[show].value_counts().plot(kind= 'bar', color= 'white', label= 'show')
df.Neighbourhood[no_show].value_counts().plot(kind= 'bar', color= 'red', label= 'no_show', title = 'Relation between Neighbourhood and Showing Up')
plt.xlabel('City', fontsize= 16)
plt.ylabel('Show Counts', fontsize= 16)


# ### The Plot shows us that 
# patients from some cities such: (JARDIM CAMBURI, MARIA ORTIZ) had show up for their appointment with a larger number than patients from cities such AEROPORIO, ILHADO FRADE
# 
# #### WE DON'T KNOW THE EXACT DISTANCE BETWEEN EACH CITY AND THE HOSPITAL BUT STII THE NEIGHBOURHOOD FORMS A SIGNIFICANT SIGN PATIENTS ATTENDANCE

# <a id='conclusions'></a>
# ## Conclusions
# 

# ### chronic diseases Impact
# we didn't see a significant effect on patients attending due to complaining a choronic disease
# 
# ### scholarship Impact
# we didn't see a significant effect on patients attending due to scholarship enrolment
# 
# ### SMS Impact
# we didn't see a significant effect on patients attending due to recieving a reminding sms 
# 
# ### Neighbourhood Impact
# It's clear that neighbourhood had a significant effect on patients attending but due to lack of data we can't specify which cities are near from or far from the hospital
# 
# ## Limitations
# - couln't detect direct corrolation between patient attendance and many other information like gender and age
# - couln't detect exact distances between patient's different cities and hospital
# 
# ##### I See that as not expected some factors like scholarship and recieving sms or not didn't affect the percentage of patients attendance, but it's also clear that factor like the Neighbourhood had a significant effect on the  percentage of patients attendance
