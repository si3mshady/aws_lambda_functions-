from covid_19_docker_plot import ProcessCSV
from flask import Flask, render_template
import gmplot
import glob
import redis
import json
import re

app=application=Flask(__name__)


class Process_Redis_Data:
    def __init__(self):        
        self.redis_conn = redis.Redis(host='localhost',port=6379)
        self.us_center = (39.587522, -101.040949)
        self.zoom = 3
        self.pcsv = ProcessCSV()
        self.load_redis_kvp()
        self.load_geo_referencing_data()
        self.gmap = self.set_gmplot()
        self.file_count = self.local_file_count()

    def set_gmplot(self) -> gmplot:
            return gmplot.GoogleMapPlotter(self.us_center[0],\
                self.us_center[1],self.zoom)

    def local_file_count(self) -> int:
        return len(glob.glob('*')) 

    def format_string_for_dictionary_processing(self,string) -> dict:
        return json.loads(re.sub(r"\'",'\"',string))

    def load_redis_kvp(self) -> None:                     
        dictionary = self.pcsv.map_cites_states_lats_longs()
        for k,v in dictionary.items():
            self.redis_conn.set(str(k),str(v))

    def fetch_city_state_lat_long(self,city,state) -> tuple:
        results = str(self.redis_conn.get(f"{city.title()},{state.title()}").decode())
        results = self.format_string_for_dictionary_processing(results)
        return results['Longitude'],results['Latitude']

    def load_geo_referencing_data(self) -> None:       
        dictionary = self.pcsv.map_cites_states_lats_longs()
        for city_state ,value in dictionary.items():           
            self.redis_conn.geoadd("locations",value['Longitude'],value['Latitude'],city_state)

    def fetch_and_plot_matches_within_x_radius(self,city,state,radius=100):   
        dictionary = self.pcsv.map_cites_states_lats_longs()
        longitude,latitude = self.fetch_city_state_lat_long(city,state)    
        results = self.redis_conn.georadius('locations',longitude, latitude,radius,'mi')
        results_decoded = [r.decode() for r in results]
        result = list(self.plot_matches_google_maps(results_decoded))       
        file_name = self.complile_lats_longs_heat_map(result)
        return file_name

    def plot_matches_google_maps(self,dictionary):
        for cured_key in dictionary:
            for key,value in self.pcsv.map_cites_states_lats_longs().items():
                if cured_key in key:
                    yield value


    def complile_lats_longs_heat_map(self,cured_dictionary) -> str:        
        lats =  [lat['Latitude'] for lat in cured_dictionary]
        longs = [lat['Longitude'] for lat in cured_dictionary]    
        self.gmap.heatmap(lats,longs)
        self.gmap.draw(f'templates/heat_plot_{self.file_count}.html')
        file_name = f"heat_plot_{self.file_count}.html"
        return file_name


@app.route('/covid19/<city>/<state>')
def elliott_lamar_arnold_processes_google_heat_map(city,state):
    processor = Process_Redis_Data()
    file_name = str(processor.fetch_and_plot_matches_within_x_radius(city,state,radius=100))
    return render_template(file_name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)



#Covid19 redis gmplot basic flask pt.3 
#Use redis geoadd and georadius to load and extract data based on radius of target city/state
#Elliott Arnold  4-25-20







#load redis with comprehensive geodata
#uset 'get' method to extract key 'City,State'
#with key value pair extract coordinates of l

#https://github.com/ajeetraina/redis/blob/master/os/mac/demo/app.py
#https://stackoverflow.com/questions/22255589/get-all-keys-in-redis-database-with-python
#https://redis-py.readthedocs.io/en/latest/_modules/redis/client.html#Redis.hget
#https://lp.redislabs.com/rs/915-NFD-128/images/WP-RedisLabs-Geospatial-Redis.pdf 
#https://pypi.org/project/redis-py-with-geo/
#https://buildmedia.readthedocs.org/media/pdf/redis-py/latest/redis-py.pdf