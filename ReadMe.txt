Since the OSM File was too big too upload, Kindly download it from here:

URL: https://s3.amazonaws.com/metro-extracts.mapzen.com/san-francisco-bay_california.osm.bz2

Unzip the san-francisco-bay_california.osm.bz2 first and then run the scripts in follwing order.

Order of Execution of Scripts:

1. data.py - To generate a sample file from the orignal osm file
2. categarization.py - Exploring data looking for problematic tags
3. audit.py - Auditing Street Names and Updating them
4. schema.py - Schema for the database
5. shaping_elements.py - Shape node elements to csv files
6. csv_to_db.py - Loading csv files in database
7. file_sizes.py - To get File Sizes Programatically
8. query_postal_codes.py - A test query to get Postal Codes along with their counts. 



 

