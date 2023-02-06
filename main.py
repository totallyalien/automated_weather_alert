import requests
meter = {
    "apikey":"YY5hEbWO1YOQH1eivOIHFFTwm4u1yzV0"
}

response = requests.get(url="http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/2805916",params=meter)
data = response.json()
has_prec = [data[i]["HasPrecipitation"] for i in range(12)]
pro_prec = [data[i]["PrecipitationProbability"] for i in range(12)]
temp =[data[i]["Temperature"]["Value"] for i in range(12)]
print(has_prec,pro_prec,temp)


def f_t(far:bool)->bool:
    return (far - 32) * 5/9