# BGP_routeviews_scrapper

This repository is for the download of BGP advertisements and infering conclusions from them over the years.

Steps involved in the process are:
1. Download the required RIBs using the script scrapper.py.
2. Extract the ribs first using:

tar -xvf <rib-file.bz2>

3. Extract the extracted ribs using zebra-dump-parser.
4. The extracted rib-dumps should be combined, to find the combined list of ribs for a particular year through multiple places.
5. The combined ribs must have many duplicate nodes. This means that multiple route-collectors might be capturing a single bgp-advertisement. The duplicates must be removed using the following command:

sort -u <combined-file-name.txt>

6. The sorted files now have the problem of AS-prepending. This must be reduced using PATH-CLEANING. The file required is file-path-cleaning.py.
7. Now we require the AS-Relationship file for the particular years. This means that for the analysis of an year, we require the relationship file for that year.
8. Based on the relationship file, we find the valleys in the file using the valley-in-file.py
