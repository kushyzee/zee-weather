from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    
    # check for empty strings or strings with only spaces
    if not bool(city.strip()):
        city = "Benin City"
        
    weather_data = get_current_weather(city)
    
    # city not found by API
    if not weather_data['cod'] == 200:
        return render_template('city-not-found.html')
    
    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{round(weather_data['main']['temp'])}",
        feels_like=f"{round(weather_data['main']['feels_like'])}"
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)