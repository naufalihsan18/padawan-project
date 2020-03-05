#!/usr/bin/env python
# coding: utf-8

# In[3]:


#project = The Padawan Project
#owner =  naufalihsan18
#import library

from arcgis.gis import GIS
from arcgis.geocoding import Geocoder, get_geocoders, geocode, reverse_geocode
import pandas as pd
from arcgis.features import FeatureLayer
from arcgis.geometry import *

gis = GIS("https://www.arcgis.com")


# In[4]:


#input area name
#geocode area address into coordinate
#append into a list

ask_more= "1"
list_daerah = []

while ask_more == "1":
    confirmation = "2"
    
    while confirmation == "2":    
        place = input ("Type name of an area or a place: ")
        g1 = geocode(place) [0]
        print (g1['address'])
        confirmation = input ("Is this the right area/place? Type 1 if true, type 2 if false: ")
        if  confirmation == "2":
            print("Please provide additional details")
            
    list_daerah.append(g1['location'])
        
    ask_more = input("Do you want to add more area or place? Type 1 if yes, type 2 if no: ")


# In[5]:


list_daerah


# In[6]:


#convert into dataframe
df_daerah = pd.DataFrame(list_daerah)

df_daerah


# In[7]:


#calculate the center of points

xmax = df_daerah['x'].max()
xmin = df_daerah['x'].min()
ymax = df_daerah['y'].max()
ymin = df_daerah['y'].min()

xcen = (xmax+xmin)/2
ycen = (ymax+ymin)/2

print(xcen, ycen)


# In[8]:


#plot into map

map1 = gis.map()

map1.center = [ycen , xcen]

#the higher the zoom value, the map will be more zoomed in
map1.zoom = 15
map1.basemap = 'osm'

#add osm restaurant layer (only Greater Jakarta area)
fs_url= 'https://services8.arcgis.com/mpSDBlkEzjS62WgX/arcgis/rest/services/OSM_restaurant/FeatureServer/0'
feature_layer = FeatureLayer(fs_url)

map1.add_layer(feature_layer)
map1


# In[9]:


#reverse geocode from point to address
name_result = reverse_geocode([xcen, ycen])
selected_area = name_result['address']['Match_addr']


# In[10]:


#create bounding box for querying results
xmin_map = map1.extent['xmin']
xmax_map = map1.extent['xmax']
ymin_map = map1.extent['ymin']
ymax_map = map1.extent['ymax']
spatial_ref = map1.extent['spatialReference']['latestWkid']

query_json = {
    'rings' : [[
        [xmax_map,ymax_map], 
        [xmax_map,ymin_map], 
        [xmin_map,ymin_map],
        [xmin_map,ymax_map],
        [xmax_map,ymax_map]
        ]],
      'spatialReference' : {"wkid" : spatial_ref}
    }
query_polygon = Polygon(query_json);
print(query_polygon)


# In[11]:


#query point based on the bounding box
query_result = feature_layer.query(geometry_filter = filters.intersects(query_polygon))
total_result = len(query_result.features)
name_result = reverse_geocode([xcen, ycen])

print("Your middle point will be around: " + selected_area)

if total_result == 0:
    print ("There is no meeting point in this area, please reduce your zoom level")
else:
    print ("There is " + str(total_result) +" meeting point(s) in this area")
    for feature in query_result.features:
        print("Name: " + str(feature.attributes['name']) + ", Type: " + str(feature.attributes['amenity']))


# In[ ]:




