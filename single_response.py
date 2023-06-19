#importing the required libraries
import requests
import json
import pandas as pd
import html
import geojson
from collections import defaultdict
import ast

#API endpoints
osmcha_base_url = "https://osmcha.org/api/v1/changesets/"
changeset_base_url="https://s3.amazonaws.com/mapbox/real-changesets/production"

#query parameters for three different districts
areas=[
  {'place':'kathmandu', 'params':'page=1&page_size=500&date__gte=2023-05-07&date__lte=2023-06-07&geometry=%7B%22type%22%3A%22Polygon%22%2C%22coordinates%22%3A%5B%5B%5B85.188235%2C27.681436%5D%2C%5B85.231539%2C27.652482%5D%2C%5B85.222017%2C27.629166%5D%2C%5B85.240128%2C27.580375%5D%2C%5B85.266427%2C27.570175%5D%2C%5B85.294522%2C27.603775%5D%2C%5B85.28236%2C27.644198%5D%2C%5B85.303252%2C27.692226%5D%2C%5B85.351794%2C27.667949%5D%2C%5B85.421414%2C27.724067%5D%2C%5B85.524809%2C27.725472%5D%2C%5B85.538154%2C27.754919%5D%2C%5B85.565476%2C27.764509%5D%2C%5B85.531477%2C27.792586%5D%2C%5B85.473174%2C27.778142%5D%2C%5B85.450199%2C27.817911%5D%2C%5B85.298667%2C27.812433%5D%2C%5B85.251658%2C27.775176%5D%2C%5B85.26749%2C27.746075%5D%2C%5B85.214604%2C27.73766%5D%2C%5B85.222193%2C27.728295%5D%2C%5B85.19801%2C27.71694%5D%2C%5B85.188235%2C27.681436%5D%5D%5D%7D'},
  {'place':'lalitpur', 'params':'page=1&page_size=500&date__gte=2023-05-07&date__lte=2023-06-07&geometry=%7B%22type%22%3A%22Polygon%22%2C%22coordinates%22%3A%5B%5B%5B85.231619%2C27.536508%5D%2C%5B85.250838%2C27.528763%5D%2C%5B85.234537%2C27.5048%5D%2C%5B85.264274%2C27.454209%5D%2C%5B85.301622%2C27.450906%5D%2C%5B85.384826%2C27.407751%5D%2C%5B85.418441%2C27.408562%5D%2C%5B85.418285%2C27.444528%5D%2C%5B85.406543%2C27.448037%5D%2C%5B85.443213%2C27.47963%5D%2C%5B85.440379%2C27.532224%5D%2C%5B85.386713%2C27.563288%5D%2C%5B85.402472%2C27.602645%5D%2C%5B85.416854%2C27.606955%5D%2C%5B85.422262%2C27.592966%5D%2C%5B85.43547%2C27.609175%5D%2C%5B85.360723%2C27.669094%5D%2C%5B85.302357%2C27.69146%5D%2C%5B85.28236%2C27.644198%5D%2C%5B85.291887%2C27.597408%5D%2C%5B85.231619%2C27.536508%5D%5D%5D%7D%2Cvalue%3A%7Btype%3APolygon%2Ccoordinates%3A%5B%5B%5B85.231619%2C27.536508%5D%2C%5B85.250838%2C27.528763%5D%2C%5B85.234537%2C27.5048%5D%2C%5B85.264274%2C27.454209%5D%2C%5B85.301622%2C27.450906%5D%2C%5B85.384826%2C27.407751%5D%2C%5B85.418441%2C27.408562%5D%2C%5B85.418285%2C27.444528%5D%2C%5B85.406543%2C27.448037%5D%2C%5B85.443213%2C27.47963%5D%2C%5B85.440379%2C27.532224%5D%2C%5B85.386713%2C27.563288%5D%2C%5B85.402472%2C27.602645%5D%2C%5B85.416854%2C27.606955%5D%2C%5B85.422262%2C27.592966%5D%2C%5B85.43547%2C27.609175%5D%2C%5B85.360723%2C27.669094%5D%2C%5B85.302357%2C27.69146%5D%2C%5B85.28236%2C27.644198%5D%2C%5B85.291887%2C27.597408%5D%2C%5B85.231619%2C27.536508%5D%5D%5D%7D'},
  {'place':'bhaktapur','params':'page=1&page_size=500&date__gte=2023-05-07&date__lte=2023-06-07&geometry=%7B%22type%22%3A%22Polygon%22%2C%22coordinates%22%3A%5B%5B%5B85.352034%2C27.668049%5D%2C%5B85.418158%2C27.620213%5D%2C%5B85.453568%2C27.636361%5D%2C%5B85.463736%2C27.625603%5D%2C%5B85.492805%2C27.652438%5D%2C%5B85.503014%2C27.68949%5D%2C%5B85.521441%2C27.694738%5D%2C%5B85.524809%2C27.725472%5D%2C%5B85.421414%2C27.724067%5D%2C%5B85.352034%2C27.668049%5D%5D%5D%7D%2Cvalue%3A%7Btype%3APolygon%2Ccoordinates%3A%5B%5B%5B85.352034%2C27.668049%5D%2C%5B85.418158%2C27.620213%5D%2C%5B85.453568%2C27.636361%5D%2C%5B85.463736%2C27.625603%5D%2C%5B85.492805%2C27.652438%5D%2C%5B85.503014%2C27.68949%5D%2C%5B85.521441%2C27.694738%5D%2C%5B85.524809%2C27.725472%5D%2C%5B85.421414%2C27.724067%5D%2C%5B85.352034%2C27.668049%5D%5D%5D%7D'}
]

#OSMcha token id
headers = {"Authorization": "Token Token_id"}

#storing all the response in a single list
osmcha_responses=[]
for area in areas:
    url = osmcha_base_url + "?" + area["params"]
    response = requests.get(url, headers=headers)
    osmcha_responses.append(response.json())

    while 'next' in response.json() and response.json()['next'] is not None:
        next_url = response.json()['next']
        response = requests.get(next_url, headers=headers)
        osmcha_responses.append(response.json())

#merging all the dictionaries in the list into one
data = {
    'type': 'FeatureCollection',
    'count': 0,
    'features': []
}

unique_ids = set()

for response in osmcha_responses:
    for feature in response['features']:
        feature_id = feature['id']
        if feature_id not in unique_ids:
            data['features'].append(feature)
            unique_ids.add(feature_id)
            data['count'] += 1


#Getting all the changes seen according to the date, area and tag(place=neighbourhood)
changes=[]
ids=[]
for item in data['features']:
  try:
    if ('neighbourhood' in item['properties']['tag_changes']['place']):
        ids.append(item['id'])
        changes.append(item)
  except:
    pass

#getting the required information from the features 
changes_list = []
openstreeturl="https://www.openstreetmap.org/{}/{}"
for feature in changes:
    changeset_id = str(feature['id'])
    changeset_url = f"{changeset_base_url}/{changeset_id}.json"
    date = feature['properties']['date']

    response = requests.get(changeset_url)
    changeset_data = response.json()

    for x in changeset_data['elements']:
        new_geometry = []
        old_geometry = []
        if x['changeset'] == changeset_id:
            feature_id = x['id']
            if 'tags' in x:            
                n_tags = x['tags']
                if isinstance(n_tags, str):
                    try:
                        n_tags = ast.literal_eval(n_tags.replace("'", '"'))
                    except (ValueError, SyntaxError):
                        n_tags = {}
            else:
                n_tags = {}

            if 'old' in x:
                old_tags = x['old']['tags']
                if isinstance(old_tags, str):
                    try:
                        old_tags = ast.literal_eval(old_tags.replace("'", '"'))
                    except (ValueError, SyntaxError):
                        old_tags = {}
            else:
                old_tags = {}

            if 'name:en' in x['tags']:
                name_value = x['tags']['name:en']
            else:
                name_value = "-"


            coordinates = []
            old_coordinates = []
            if x['type']=='node' and 'lat' in x and 'lon' in x:
                coordinates.append((float(x['lon']), float(x['lat'])))
            elif 'nodes' in x:
                for node in x["nodes"]:
                    coordinates.append((float(node["lon"]), float(node["lat"])))
            if 'old' in x:
                if x['old']['type']=='node' and 'lat' in x['old'] and 'lon' in x['old']:
                    old_coordinates.append((float(x['old']['lon']), float(x['old']['lat'])))
                elif 'old' in x and 'nodes' in x['old']:
                    for node in x['old']["nodes"]:
                        old_coordinates.append((float(node["lon"]), float(node["lat"])))

            geometry = geojson.LineString(coordinates) if x["type"] == "way" else geojson.Point([coordinates])
            feature_geojson = geojson.Feature(geometry=geometry, properties={})
            new_geometry.append(feature_geojson)

            geometry_1 = geojson.LineString(old_coordinates) if x["type"] == "way" else geojson.Point([old_coordinates])
            feature_geojson = geojson.Feature(geometry=geometry_1, properties={})
            old_geometry.append(feature_geojson)
            geometry_changed = "No"
            if coordinates != old_coordinates:
                geometry_changed = "Yes"
            

            if any(key == 'place' and value == 'neighbourhood' for key, value in old_tags.items()):
                changes = {
                    'changeset_id': x['changeset'],
                    'feature_id': feature_id,
                    'user': x['user'],
                    'user_id': x['uid'],
                    'action': x['action'],
                    'type': x.get('type', ''),
                    'old_tags': old_tags,
                    'new_tags': n_tags,
                    'date': date,
                    'name': name_value,
                    'geometry_changed': geometry_changed,
                    'viewOSM': openstreeturl.format(html.escape(x['type']), feature_id)
                }
                if geometry_changed == "Yes":
                    changes['new_geometry'] = new_geometry
                    changes['old_geometry'] = old_geometry
                else:
                    changes['new_geometry'] = new_geometry
                changes_list.append(changes)
  
            elif any(key == 'place' and value == 'neighbourhood' for key, value in n_tags.items()):
                changes = {
                    'changeset_id': x['changeset'],
                    'feature_id': feature_id,
                    'user': x['user'],
                    'user_id': x['uid'],
                    'action': x['action'],
                    'type': x.get('type', ''),
                    'old_tags': old_tags,
                    'new_tags': n_tags,
                    'date': date,
                    'name': name_value,
                    'geometry_changed': geometry_changed,
                    'viewOSM': openstreeturl.format(html.escape(x['type']), feature_id)
                }
                if geometry_changed == "Yes":
                    changes['new_geometry'] = new_geometry
                    changes['old_geometry'] = old_geometry
                else:
                    changes['new_geometry'] = new_geometry
                changes_list.append(changes)


#getting the duplicate feature id with there respective changesets
changesets = {}
for entry in changes_list:
    feature_id = entry['feature_id']
    changeset_id = entry['changeset_id']
    if feature_id not in changesets:
        changesets[feature_id] = []
    changesets[feature_id].append(changeset_id)

duplicate_changesets = {feature_id: changesets[feature_id] for feature_id in changesets if len(changesets[feature_id]) > 1}
print(duplicate_changesets)

#merging all the changesets with duplicate feature_id to get a single row of features
changeset_lists=[]
result=[]
keys=list(duplicate_changesets.keys())
print(keys)
for key,value in duplicate_changesets.items():
  changeset_lists=value
  changeset_lists.sort()
  print(changeset_lists)
  old_changeset=changeset_lists[0]
  print(old_changeset)
  latest_changeset=changeset_lists[-1]
  print(latest_changeset)
  url1=f"https://s3.amazonaws.com/mapbox/real-changesets/production/{latest_changeset}.json"
  url=f"https://s3.amazonaws.com/mapbox/real-changesets/production/{old_changeset}.json"
  print(url)
  print(url1)
  response=requests.get(url)
  output=response.json()
  response=requests.get(url1)
  output1=response.json()
  date = feature['properties']['date']
  for x in output['elements']:
      old_geometry = []
      tags=x['tags']
      if x['changeset'] == old_changeset and any(key == 'place' and value == 'neighbourhood' for key, value in tags.items()):
          if 'old' in x:
              old_tags = x['old']['tags']
          else:
              old_tags = "-"
          coordinates = []
          if 'old' in x:
            if x['type'] == 'way' and 'nodes' in x['old']:
                for node in x['old']['nodes']:
                    coordinates.append((float(node['lon']), float(node['lat'])))
            elif x['type'] == 'node':
                coordinates.append((float(x['old']['lon']), float(x['old']['lat'])))
                print(coordinates)
          if len(coordinates) > 0:
              if x["type"] == "way":
                    geometry_1 = geojson.LineString(coordinates) if len(coordinates) > 1 else geojson.Point(coordinates[0])
              else:
                    geometry_1 = geojson.Point(coordinates[0])
              feature_geojson = geojson.Feature(geometry=geometry_1, properties={})
              old_geometry.append(feature_geojson)
  for x in output1['elements']:
      feature_id = x['id']
      new_geometry = []
      tags = x['tags']
      if x['changeset'] == latest_changeset and x['id'] in keys and any(key == 'place' and value == 'neighbourhood' for key, value in tags.items()):
          tags = x['tags']
          if 'name:en' in x['tags']:
                name_value = x['tags']['name:en']
          else:
                name_value = "-"
          new_coordinates = []
          if x['type'] == 'way' and 'nodes' in x:
              for node in x['nodes']:
                new_coordinates.append((float(node['lon']), float(node['lat'])))
          elif x['type'] == 'node':
                new_coordinates.append((float(x['lon']), float(x['lat'])))

          if x["type"] == "way":
            geometry= geojson.LineString(new_coordinates) if len(new_coordinates) > 1 else geojson.Point(new_coordinates[0])
          else:
            geometry = geojson.Point(new_coordinates[0])
          feature_geojson_1 = geojson.Feature(geometry=geometry, properties={})
          new_geometry.append(feature_geojson_1)
          geometry_changed = "No"
          if new_coordinates != coordinates:
                geometry_changed = "Yes"
          results={
                'changeset_id': x['changeset'],
                'feature_id': feature_id,
                'user': x['user'],
                'user_id': x['uid'],
                'action': x['action'],
                'old_tags': old_tags,
                'new_tags': x['tags'],
                'date': date,
                'name': name_value,
                'geometry_changed': geometry_changed,
                'viewOSM': openstreeturl.format(html.escape(x['type']), feature_id),
                'type': x['type'],
                'new_geometry': new_geometry,
                'old_geometry': old_geometry,
            }
          if geometry_changed == "Yes":
                results['new_geometry'] = new_geometry
                results['old_geometry'] = old_geometry
          else:
                results['new_geometry'] = new_geometry
                results['old_geometry'] = '-'
          if geometry_changed == "Yes" and not old_geometry:
                results['geometry_changed'] = "No"
                results['old_geometry'] = '-'
          result.append(results)

#getting only the changesets with unique feature_id
feature_id_counts = defaultdict(int)
changes_list_filtered = []

for item in changes_list:
    feature_id = item['feature_id']
    feature_id_counts[feature_id] += 1

for item in changes_list:
    feature_id = item['feature_id']
    if feature_id_counts[feature_id] > 1:
        continue
    changes_list_filtered.append(item)


changes_list = changes_list_filtered

#making new list that adds both the list of unique feature_id and duplicate feature_id
new_list= changes_list+result

#sorting the list according to the changeset
sorted_list = sorted(new_list, key=lambda x: x['changeset_id'])

#making a Dataframe 
df=pd.DataFrame(sorted_list)

#adding three new columns to the dataframe
df['tags_added'] = ""
df['tags_removed'] = ""
df['tags_modified'] = ""

for i, row in df.iterrows():
    old_tags = row['old_tags']
    new_tags = row['new_tags']
    
    added_tags = {}
    removed_tags = {}
    modified_tags = {}

    if isinstance(old_tags, dict):
        for key, value in new_tags.items():
            if key not in old_tags:
                added_tags[key] = value
            elif old_tags[key] != value:
                modified_tags[key] = {'old': old_tags[key], 'new': value}
        
        for key, value in old_tags.items():
            if key not in new_tags:
                removed_tags[key] = value

    if not added_tags:
        added_tags = '-'
    if not removed_tags:
        removed_tags = '-'
    if not modified_tags:
        modified_tags = '-'

    df.at[i, 'tags_added'] = added_tags
    df.at[i, 'tags_removed'] = removed_tags
    df.at[i, 'tags_modified'] = modified_tags

df['tags_added'] = df['tags_added'].astype(str)
df['tags_removed'] = df['tags_removed'].astype(str)
df['tags_modified'] = df['tags_modified'].astype(str)

#desired order of the columns in Dataframe
desired_order = ['feature_id', 'name', 'type', 'action','tags_added','tags_removed','tags_modified','changeset_id','date','user','user_id','new_tags','old_tags','geometry_changed','new_geometry','old_geometry','viewOSM']
df = df.reindex(columns=desired_order)

#setting feature_id as a index column
df.set_index('feature_id', inplace=True)

#replacing all the NaN values with '-'
df.fillna('-')

#stroing all the output in place.csv
df.to_csv('place.csv')
