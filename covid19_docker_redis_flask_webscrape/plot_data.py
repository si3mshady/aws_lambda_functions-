from covid_wiki_scrapper import CV19
from covid_19_docker_plot import ProcessCSV
import gmplot
import glob 

class GPlot:
    def __init__(self):
        self.us_center = (39.587522, -101.040949)
        self.zoom = 3
        self.csv_parser = ProcessCSV()
        self.wiki_scrape = CV19()
        self.gmap = self.set_gmplot()
        self.file_count = self.local_file_count()
    
    def set_gmplot(self) -> gmplot:
        return gmplot.GoogleMapPlotter(self.us_center[0],\
            self.us_center[1],self.zoom)

    def local_file_count(self) -> int:
        return len(glob.glob('*')) 


    def complile_lats_longs_heat_map(self) -> None:
        data = list(self.wiki_csv_fusion_generator())
        lats =  [lat['Latitude'] for lat in data]
        longs = [lat['Longitude'] for lat in data]    
        self.gmap.heatmap(lats,longs)
        self.gmap.draw(f'heat_plot_{self.file_count}.html')
        
    def wiki_csv_fusion_generator(self):
        #order data by states in order to populate the lat,long lists required by gmplot
        csv_lats_longs = self.csv_parser.map_cites_states_lats_longs()
        wiki_scrapped_data = self.wiki_scrape.make_data_documents()
        for wiki in wiki_scrapped_data:
            for entry in csv_lats_longs.values():
                if wiki in entry['State']:
                    yield entry


if __name__ == "__main__":
    test = GPlot()
    test.complile_lats_longs_heat_map


#get the center of the country -> Kansas 39.587522, -101.040949
#Google Map Plotter 1-3 zoom 
#use heatmap 

    
