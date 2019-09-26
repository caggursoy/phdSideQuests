from google_images_search import GoogleImagesSearch

gis = GoogleImagesSearch('AIzaSyDsZwDya5BKwCDNy6JOnCVSr6u4Rk_F4u8', 'cx=001638208462104285707:u7lukw8ynbl')

#define search params:
_search_params = {
    'q': '...',
    'num': 1-50,
    'safe': 'high|medium|off',
    'fileType': 'jpg|gif|png',
    'imgType': 'clipart|face|lineart|news|photo',
    'imgSize': 'huge|icon|large|medium|small|xlarge|xxlarge',
    'imgDominantColor': 'black|blue|brown|gray|green|pink|purple|teal|white|yellow'
}

# # this will only search for images:
# gis.search(search_params=_search_params)
#
# # this will search and download:
# gis.search(search_params=_search_params, path_to_dir='/path/')
#
# # this will search, download and resize:
# gis.search(search_params=_search_params, path_to_dir='/path/', width=500, height=500)

# search first, then download and resize afterwards
gis.search(search_params=_search_params)
for image in gis.results():
    image.download('/searchResults/')
    image.resize(200, 200)
