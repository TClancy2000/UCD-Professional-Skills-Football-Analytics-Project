#!/usr/bin/env python
# coding: utf-8

# #Load relevant Librarires

# In[7]:


import pandas as pd
from pandas import json_normalize
import requests


# #Load "competitions" structure file from GitHub

# In[8]:


competitions = requests.get('http://raw.githubusercontent.com/statsbomb/open-data/master/data/competitions.json')
competitions = competitions.json()
                            


# In[37]:


competitions


# #sorting python structures

# In[13]:


for competition in competitions:
    print(competition['competition_name'],competition['season_name'],competition['competition_id'],competition['season_id'])


# #Locating dataframes using the competition id and season id for most recent la liga season

# In[14]:


competition_id = 11
season_id = 90


# #Load Matches using the "ID" strings in the "matches" structure

# In[17]:


matches = requests.get('https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/'+str(competition_id)+'/'+str(season_id)+'.json')
matches = matches.json()


# In[18]:


matches


# Sort by strings in order to find individual data sets in Ids for home and away fixtures

# In[29]:


for match in matches:
    print(match['home_team']['home_team_name'], match['away_team']['away_team_name']+             " " + str(match['home_score']) + ":" +str(match['away_score']) + " (match_id is " + str(match['match_id']) + ")")


# #Located match_id's = 3773585 and 3773497

# #Score 3773585 is Barcelona 1:3 Madrid

# In[31]:


match_id = 3773585


# In[34]:


events = requests.get('https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/'+str(match_id)+'.json')


# In[35]:


events = events.json()
events


# In[36]:


#use Pandas to tabulate the dataframe


# In[40]:


events = json_normalize(events, sep = "_")


# In[42]:


events.head(5)


# In[43]:


pd.set_option("display.max.columns", None)


# In[44]:


events.head(5)


# Fixture Stats Breakdown by Team

# In[45]:


events['type_name'].value_counts()


# In[46]:


barcelona = events.loc[events['possession_team_name'] == 'Barcelona']
barcelona['type_name'].value_counts()


# In[47]:


madrid = events.loc[events['possession_team_name'] == 'Real Madrid']
madrid['type_name'].value_counts()


# In[64]:


import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
import numpy as np
import requests


# In[66]:


df = events.loc[events['possession_team_name'] == 'Barcelona']


# In[67]:


barcelona_passes = df.loc[(df['type_name'] == "Pass") & (df['team_name'] == "Barcelona")]


# In[68]:


barcelona_passes.head(5)


# In[98]:


def createPitch():
    
    #Create figure
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)

    #Pitch Outline & Centre Line
    plt.plot([0,0],[0,90], color="black")
    plt.plot([0,130],[90,90], color="black")
    plt.plot([130,130],[90,0], color="black")
    plt.plot([130,0],[0,0], color="black")
    plt.plot([65,65],[0,90], color="black")
    
    #Left Penalty Area
    plt.plot([16.5,16.5],[65,25],color="black")
    plt.plot([0,16.5],[65,65],color="black")
    plt.plot([16.5,0],[25,25],color="black")
    
    #Right Penalty Area
    plt.plot([130,113.5],[65,65],color="black")
    plt.plot([113.5,113.5],[65,25],color="black")
    plt.plot([113.5,130],[25,25],color="black")
    
    #Left 6-yard Box
    plt.plot([0,5.5],[54,54],color="black")
    plt.plot([5.5,5.5],[54,36],color="black")
    plt.plot([5.5,0.5],[36,36],color="black")
    
    #Right 6-yard Box
    plt.plot([130,124.5],[54,54],color="black")
    plt.plot([124.5,124.5],[54,36],color="black")
    plt.plot([124.5,130],[36,36],color="black")
    
    #Prepare Circles
    centreCircle = plt.Circle((65,45),9.15,color="black",fill=False)
    centreSpot = plt.Circle((65,45),0.8,color="black")
    leftPenSpot = plt.Circle((11,45),0.8,color="black")
    rightPenSpot = plt.Circle((119,45),0.8,color="black")
    
    #Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)
    
    
    #Tidy Axes
    plt.axis('off')
    
    #Display Pitch
    plt.show()
    
createPitch()


# Pass Plot Barcelona 1:3 Madrid 

# In[119]:


#plt.gca()invert_yaxis()

#for x in range (15)
for x in range (len(barcelona_passes['id'])):
    #we can choose 1, 2 or both
    if barcelona_passes['period'].iloc[x] == 1 or barcelona_passes['period'].iloc[x] == 2:
        if any ([barcelona_passes['pass_outcome_name'].iloc[x] == 'Incomplete', barcelona_passes['pass_outcome_name'].iloc[x] == 'Out',
                 barcelona_passes['pass_outcome_name'].iloc[x] == 'Unknown', barcelona_passes['pass_outcome_name'].iloc[x] == 'Pass Offside',
                 barcelona_passes['pass_outcome_name'].iloc[x] == 'Injury Clearance']):
            
            
            plt.plot((barcelona_passes['location'].iloc[x][0], barcelona_passes['pass_end_location'].iloc[x][0]),                     (barcelona_passes['location'].iloc[x][1], barcelona_passes['pass_end_location'].iloc[x][1]),color='red')
            
            plt.scatter(barcelona_passes['location'].iloc[x][1], barcelona_passes['pass_end_location'].iloc[x][1],color='red',s=100)
        else:
        
            plt.plot((barcelona_passes['location'].iloc[x][0], barcelona_passes['pass_end_location'].iloc[x][0]),                     (barcelona_passes['location'].iloc[x][1], barcelona_passes['pass_end_location'].iloc[x][1]),color='blue')
        
            plt.scatter(barcelona_passes['location'].iloc[x][1], barcelona_passes['pass_end_location'].iloc[x][1],color='blue', s=100)
        
        
    


# #Score 3773497 = Barcelona 1: Madrid 2

# In[120]:


match_id = 3773497


# In[121]:


events = requests.get('https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/'+str(match_id)+'.json')


# In[122]:


events = events.json()
events


# In[123]:


events = json_normalize(events, sep = "_")


# In[124]:


events.head(5)


# Fixture Stats Breakdown by Team 

# In[125]:


events['type_name'].value_counts()


# In[126]:


barcelona = events.loc[events['possession_team_name'] == 'Barcelona']
barcelona['type_name'].value_counts()


# In[127]:


madrid = events.loc[events['possession_team_name'] == 'Real Madrid']
madrid['type_name'].value_counts()


# In[128]:


df = events.loc[events['possession_team_name'] == 'Barcelona']


# In[129]:


barcelona_passes = df.loc[(df['type_name'] == "Pass") & (df['team_name'] == "Barcelona")]


# In[130]:


barcelona_passes.head(5)


# In[131]:


def createPitch():
    
    #Create figure
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)

    #Pitch Outline & Centre Line
    plt.plot([0,0],[0,90], color="black")
    plt.plot([0,130],[90,90], color="black")
    plt.plot([130,130],[90,0], color="black")
    plt.plot([130,0],[0,0], color="black")
    plt.plot([65,65],[0,90], color="black")
    
    #Left Penalty Area
    plt.plot([16.5,16.5],[65,25],color="black")
    plt.plot([0,16.5],[65,65],color="black")
    plt.plot([16.5,0],[25,25],color="black")
    
    #Right Penalty Area
    plt.plot([130,113.5],[65,65],color="black")
    plt.plot([113.5,113.5],[65,25],color="black")
    plt.plot([113.5,130],[25,25],color="black")
    
    #Left 6-yard Box
    plt.plot([0,5.5],[54,54],color="black")
    plt.plot([5.5,5.5],[54,36],color="black")
    plt.plot([5.5,0.5],[36,36],color="black")
    
    #Right 6-yard Box
    plt.plot([130,124.5],[54,54],color="black")
    plt.plot([124.5,124.5],[54,36],color="black")
    plt.plot([124.5,130],[36,36],color="black")
    
    #Prepare Circles
    centreCircle = plt.Circle((65,45),9.15,color="black",fill=False)
    centreSpot = plt.Circle((65,45),0.8,color="black")
    leftPenSpot = plt.Circle((11,45),0.8,color="black")
    rightPenSpot = plt.Circle((119,45),0.8,color="black")
    
    #Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)
    
    
    #Tidy Axes
    plt.axis('off')
    
    #Display Pitch
    plt.show()
    
createPitch()


# Pass Plot Barcelona 1:2 Madrid

# In[132]:


#plt.gca()invert_yaxis()

#for x in range (15)
for x in range (len(barcelona_passes['id'])):
    #we can choose 1, 2 or both
    if barcelona_passes['period'].iloc[x] == 1 or barcelona_passes['period'].iloc[x] == 2:
        if any ([barcelona_passes['pass_outcome_name'].iloc[x] == 'Incomplete', barcelona_passes['pass_outcome_name'].iloc[x] == 'Out',
                 barcelona_passes['pass_outcome_name'].iloc[x] == 'Unknown', barcelona_passes['pass_outcome_name'].iloc[x] == 'Pass Offside',
                 barcelona_passes['pass_outcome_name'].iloc[x] == 'Injury Clearance']):
            
            
            plt.plot((barcelona_passes['location'].iloc[x][0], barcelona_passes['pass_end_location'].iloc[x][0]),                     (barcelona_passes['location'].iloc[x][1], barcelona_passes['pass_end_location'].iloc[x][1]),color='red')
            
            plt.scatter(barcelona_passes['location'].iloc[x][1], barcelona_passes['pass_end_location'].iloc[x][1],color='red',s=100)
        else:
        
            plt.plot((barcelona_passes['location'].iloc[x][0], barcelona_passes['pass_end_location'].iloc[x][0]),                     (barcelona_passes['location'].iloc[x][1], barcelona_passes['pass_end_location'].iloc[x][1]),color='blue')
        
            plt.scatter(barcelona_passes['location'].iloc[x][1], barcelona_passes['pass_end_location'].iloc[x][1],color='blue', s=100)
        
        
    


# In[ ]:




