import os


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

file_size_nodes = convert_bytes(os.path.getsize('nodes.csv'))
file_size_nodestags = convert_bytes(os.path.getsize('nodes_tags.csv'))
file_size_ways = convert_bytes(os.path.getsize('ways.csv'))
file_size_waysnodes = convert_bytes(os.path.getsize('ways_nodes.csv'))
file_size_waystags = convert_bytes(os.path.getsize('ways_tags.csv'))
file_size_osmfile = convert_bytes(os.path.getsize('san-francisco-bay_california.osm'))
file_size_samplefile = convert_bytes(os.path.getsize('sample_san-francisco-bay_california.osm'))
file_size_db = convert_bytes(os.path.getsize('SanFrancisco.db'))

print("OSM File: " + str(file_size_osmfile))
print("Sample File: " + str(file_size_samplefile))
print("Database Size: " + str(file_size_db))
print("Nodes.csv: " + str(file_size_nodes))
print("Nodes_tagss.csv: " + str(file_size_nodestags))
print("Ways.csv: " + str(file_size_ways))
print("Ways_tags.csv: " + str(file_size_waystags))
print("Ways_nodes.csv: " + str(file_size_waysnodes))