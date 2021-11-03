import datetime
import requests
from dateutil import parser as dparser


# requires python 3.6+ for fstrings

class PinballMap():

    def __init__(self, *args, **kwargs):
        """eventually will have more of the api, but this is all I need right now"""
        pass

    def fetch_locations_for_a_single_region(self, *args, **kwargs):
        # 	Fetch locations for a single region

        region = kwargs.get('region')
        url = f"""https://pinballmap.com/api/v1/region/{region}/locations.json"""
        r = requests.get(url)

        return r.json()

    def fetch_all_regions(self, *args, **kwargs):
        # 	Fetch all regions

        url = """https://pinballmap.com/api/v1/regions.json"""
        r = requests.get(url, *args, **kwargs)
        return r.json()


class PinballmapMachine():

    def __init__(self, data):

        self._doc = data
        for k in ['created_at', 'updated_at']:
            data[k] = dparser.parse(data[k])

        self.__dict__.update(data)

        s = ['ipdb_id', 'ipdb_link', 'machine_group_id',
             'manufacturer', 'name', 'opdb_id', 'year']

        for k in s:

            prop = k
            while prop in data:
                prop = 'machine_' + prop
            setattr(self, prop, data['machine'][k])


class PinballmapLocation():

    def __init__(self, data):
        for k in ['created_at', 'updated_at']:
            data[k] = dparser.parse(data[k])
        data['scanned_at'] = datetime.datetime.now()
        self._doc = data

        self.__dict__.update(data)
        self.machines = [PinballmapMachine(m)
                         for m in self.location_machine_xrefs]

    @property
    def map_link(self):
        url = f"""https://pinballmap.com/map?by_location_id={self.id}"""
        return url

    def __str__(self):
        return self.__dict__.get('name', 'name not defined')


def dump_region_locations_by_last_updated(region):
    p = PinballMap()
    region_locations = p.fetch_locations_for_a_single_region(region=region)

    locations = [PinballmapLocation(l) for l in region_locations['locations']]
    for l in sorted(locations, key=lambda x: x.updated_at):
        print(l.num_machines, l.city, l, l.updated_at, l.map_link, l.website)


def list_all_regions():
    p = PinballMap()
    for region in sorted(p.fetch_all_regions()['regions'], key=lambda x: x['name']):
        print(region['name'], region['id'])


if __name__ == '__main__':
    dump_region_locations_by_last_updated(region='philadelphia')

"""

    pinballmap.com API 1.0 

If you use this API for something cool, please let us know, we like looking at interesting uses of the data. If you have any suggestions/requests for endpoints, please email: scott.wainstock@gmail.com. If you have any patches that you'd like to submit to the API, please check out: github.com/scottwainstock/pbm.
Resources
Events
Resource 	Description
GET /api/v1/region/:region/events.json 	Get all events for a single region
Location machine xrefs
Resource 	Description
GET /api/v1/region/:region/location_machine_xrefs.json 	Get all machines at locations in a single region
GET /api/v1/location_machine_xrefs/:id.json 	Get info about a single lmx
POST /api/v1/location_machine_xrefs.json 	Find or create a machine at a location
PUT /api/v1/location_machine_xrefs/:id.json 	Update a machine's condition at a location
DESTROY /api/v1/location_machine_xrefs/:id.json 	Remove a machine from a location
GET /api/v1/location_machine_xrefs/top_n_machines.json 	Show the top N machines on location
Location types
Resource 	Description
GET /api/v1/location_types.json 	Fetch all location types
Locations
Resource 	Description
POST /api/v1/locations/suggest.json 	Suggest a new location to add to the map
GET /api/v1/locations.json 	Fetch locations for all regions
GET /api/v1/region/:region/locations.json 	Fetch locations for a single region
PUT /api/v1/locations/:id.json 	Update attributes on a location
GET /api/v1/locations/closest_by_lat_lon.json 	Returns the closest location to transmitted lat/lon
GET /api/v1/locations/closest_by_address.json 	Returns the closest location to transmitted address
GET /api/v1/locations/:id.json 	Display the details of this location
GET /api/v1/locations/:id/machine_details.json 	Display the details of the machines at this location
PUT /api/v1/locations/:id/confirm.json 	Confirm location information
GET /api/v1/locations/autocomplete_city.json 	Send back a list of cities in the DB that fit your search criteria
GET /api/v1/locations/autocomplete.json 	Send back fuzzy search results of search params
Machine score xrefs
Resource 	Description
GET /api/v1/region/:region/machine_score_xrefs.json 	Fetch all high scores for a region
POST /api/v1/machine_score_xrefs.json 	Enter a new high score for a machine
GET /api/v1/machine_score_xrefs/:id.json 	View all high scores for a location's machine
Machines
Resource 	Description
GET /api/v1/machines.json 	Fetch all machines
POST /api/v1/machines.json 	Create a new canonical machine
Operators
Resource 	Description
GET /api/v1/operators.json 	Fetch all operators for all regions
GET /api/v1/region/:region/operators.json 	Fetch all operators
GET /api/v1/operators/:id.json 	Fetch information for a single operator
Region link xrefs
Resource 	Description
GET /api/v1/region/:region/region_link_xrefs.json 	Fetch all region-centric web sites
Regions
Resource 	Description
GET /api/v1/regions/location_and_machine_counts.json 	Get location and machine counts
GET /api/v1/regions/does_region_exist.json 	Find if name corresponds to a known region
GET /api/v1/regions/closest_by_lat_lon.json 	Find closest region based on lat/lon
GET /api/v1/regions.json 	Fetch all regions
GET /api/v1/regions/:id.json 	Fetch information for a single region
POST /api/v1/regions/suggest.json 	Suggest a new region to add to the map
POST /api/v1/regions/contact.json 	Contact regional administrator
POST /api/v1/regions/app_comment.json 	Send comments about the app
User submissions
Resource 	Description
GET /api/v1/region/:region/user_submissions.json 	Fetch user submissions for a single region
GET /api/v1/user_submissions/list_within_range.json 	Fetch user submissions within N miles of provided lat/lon
Users
Resource 	Description
GET /api/v1/users/:id/list_fave_locations.json 	Fetch list of favorite locations
POST /api/v1/users/:id/add_fave_location.json 	Adds a location to your fave list
POST /api/v1/users/:id/remove_fave_location.json 	Removes a location from your fave list
GET /api/v1/users/auth_details.json 	Fetch auth info for a user
POST /api/v1/users/forgot_password.json 	Password retrieval
POST /api/v1/users/resend_confirmation.json 	Resend confirmation
POST /api/v1/users/signup.json 	Signup a new user
GET /api/v1/users/:id/profile_info.json 	Fetch profile info for a user
Zones
Resource 	Description
GET /api/v1/region/:region/zones.json 	Fetch zones for a single region
"""
