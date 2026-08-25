from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create a `login_user` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request body
    data = json.loads(request.body)

    username = data['userName']
    password = data['password']

    # Check whether the provided credentials can be authenticated
    user = authenticate(username=username, password=password)

    data = {
        "userName": username
    }

    if user is not None:
        # If user is valid, log in the current user
        login(request, user)

        data = {
            "userName": username,
            "status": "Authenticated"
        }

    return JsonResponse(data)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Terminate user session
    logout(request)

    # Return empty username
    data = {
        "userName": ""
    }

    return JsonResponse(data)


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    # Load JSON data from the request body
    data = json.loads(request.body)

    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    username_exist = False

    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True

    except User.DoesNotExist:
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )

        # Log in the user
        login(request, user)

        data = {
            "userName": username,
            "status": "Authenticated"
        }

        return JsonResponse(data)

    else:
        data = {
            "userName": username,
            "error": "Already Registered"
        }

        return JsonResponse(data)


# Get the available cars
def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)

    # Populate the database if no CarMake records exist yet
    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')

    cars = []

    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })

    return JsonResponse({
        "CarModels": cars
    })


# Render list of dealerships.
# All dealerships are returned by default.
# If a state is passed, only dealerships in that state are returned.
def get_dealerships(request, state="All"):

    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state

    dealerships = get_request(endpoint)

    return JsonResponse({
        "status": 200,
        "dealers": dealerships
    })


# Get details for a specific dealer
def get_dealer_details(request, dealer_id):

    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)

        dealership = get_request(endpoint)

        return JsonResponse({
            "status": 200,
            "dealer": dealership
        })

    else:
        return JsonResponse({
            "status": 400,
            "message": "Bad Request"
        })


# Get reviews for a specific dealer and analyze
# the sentiment of every review.
def get_dealer_reviews(request, dealer_id):

    # If dealer id has been provided
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)

        reviews = get_request(endpoint)

        for review_detail in reviews:
            response = analyze_review_sentiments(
                review_detail['review']
            )

            print(response)

            review_detail['sentiment'] = response['sentiment']

        return JsonResponse({
            "status": 200,
            "reviews": reviews
        })

    else:
        return JsonResponse({
            "status": 400,
            "message": "Bad Request"
        })


# Create an `add_review` view to submit a review
@csrf_exempt
def add_review(request):

    if request.method != "POST":
        return JsonResponse({
            "status": 405,
            "message": "Method not allowed"
        })

    if request.user.is_anonymous is False:

        try:
            data = json.loads(request.body)

            print("Review data received:")
            print(data)

            response = post_review(data)

            print("post_review response:")
            print(response)

            return JsonResponse({
                "status": 200
            })

        except Exception as e:
            # Print the actual error in the Django terminal
            print("Error posting review:", e)

            return JsonResponse({
                "status": 401,
                "message": "Error in posting review"
            })

    else:
        return JsonResponse({
            "status": 403,
            "message": "Unauthorized"
        })