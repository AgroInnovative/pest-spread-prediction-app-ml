from django.http import HttpResponse
from django.shortcuts import render
from .models import WeatherPattern
from django.shortcuts import redirect


# ML Model Related Packages
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score  # check accuracy of the model
import joblib  # percisting the ML model
from sklearn import tree  # Visualizing in graphical format


import pyrebase
# firebase connectivity
config = {
    'apiKey': "AIzaSyBQrzJBcSghc0jURLoNup5d1CWN_p3IO10",
    'authDomain': "elzian-agro.firebaseapp.com",
    'databaseURL': "https://elzian-agro.firebaseio.com",
    'projectId': "elzian-agro",
    'storageBucket': "elzian-agro.appspot.com",
    'messagingSenderId': "1053254570239",
    'appId': "1:1053254570239:web:76162fa428bc75a3f53cca",
    'measurementId': "G-4EHN1RM1V1"
}
firebase = pyrebase.initialize_app(config)
database = firebase.database()


# ML model Training
weather_data = pd.read_csv('pest.csv')
print(weather_data)
print(weather_data.values)
X = weather_data.drop(columns=["Formatted Date", "Wind Bearing (degrees)", "Loud Cover", "Apparent Temperature (C)",
                               "Summary", "Precip Type", "Daily Summary", "Pest Disease"])
y = weather_data["Pest Disease"]
print(X)
print(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# percisting the model and saving it in a file
joblib.dump(model, "pest_spread_predictor.joblib")

# meassure the accuray of the model
predictions = model.predict(X_test)
score = accuracy_score(y_test, predictions)
print(score)

# comment out all of the above after percisting the model and use below command
# Using percisting trained model
joblib.load("pest_spread_predictor.joblib")


def getPrediction(user_id):
    # Get Prediction by using model
    # Get data from firebase
    # user_id = "iS4YR9Xb0YT3ujypGiZZipWJq332"

    usersSpecificWeather_temperature = database.child('users').child(
        user_id).child("forecastedWeather").child("temperature").get().val()

    usersSpecificWeather_windSpeed = database.child('users').child(
        user_id).child("forecastedWeather").child("windSpeed").get().val()

    usersSpecificWeather_humidity = database.child('users').child(
        user_id).child("forecastedWeather").child("humidity").get().val()

    usersSpecificWeather_visibility = database.child('users').child(
        user_id).child("forecastedWeather").child("visibility").get().val()

    usersSpecificWeather_pressure = database.child('users').child(
        user_id).child("forecastedWeather").child("pressure").get().val()

    # specific_prediction = model.predict(  # a specific test data set
    #     [[9.5348, 7.38889, 0.84, 13.65, 255, 15.4568, 1015.15]])

    specific_prediction = model.predict(  # a specific test data set
        [[usersSpecificWeather_temperature,
          usersSpecificWeather_windSpeed,
          usersSpecificWeather_humidity,
          usersSpecificWeather_visibility,
          usersSpecificWeather_pressure,
          ]])

    specific_prediction = specific_prediction[0]
    print(specific_prediction)
    print("Your cultivation is most likely to affect with " +
          specific_prediction + " in coming week")

    print("")


# Visualizing
tree.export_graphviz(model,
                     out_file='pest_predictor.dot',
                     feature_names=['Temperature (C)',
                                    'Humidity', 'Wind Speed (km/h)',
                                    'Visibility (km)',
                                    'Pressure (millibars)'],
                     class_names=sorted(y.unique()),
                     label="all",
                     rounded=True,
                     filled=True)

# Create your views here.
# print(usersSpecificWeather.name)


def index(request, user_id):
    getPrediction(user_id)
    # WeatherPatterns = WeatherPattern.objects.all()
    # output = ', '.join([w.name for w in WeatherPatterns])
    # return render(request, 'index.html', {'weatherPatterns': WeatherPatterns})
    # return HttpResponse(output)
    # return HttpResponse(output[0].name)

    # push result to firebase
    database.child('users').child(user_id).child(
        "ML_generated_pest_prediction").set(specific_prediction)
    return redirect("https://agro.elzian.com/dashboard")
    # database.child('users').child(userId).child("pest_prediction").set(specific_prediction)
    # return HttpResponse("Your cultivation is most likely to affect with "+specific_pred