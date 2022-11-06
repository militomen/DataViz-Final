import requests, json
 
# Enter your API key here
api_key = "a5199b175531f72559a9c1354f616168"
 
# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"
 
# Give city name
city_name = "Santiago,cl"
 
# complete_url variable to store
# complete url address
complete_url = base_url + "appid=" + api_key + "&q=" + city_name
 
# get method of requests module
# return response object
response = requests.get(complete_url)
 
# json method of response object
# convert json format data into
# python format data
x = response.json()
print(x)
descripcion_clima   =  x {['weather'][0],['description'],
                        ['cord'][0]
                        }
print(descripcion_clima)
