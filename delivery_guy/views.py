from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from accounts.models import DeliveryCompany, DeliveryGuy, Buyer
from delivery.models import Delivery
from orders.models import Order, OrderedProduct
import json
from django.contrib.auth.hashers import make_password
from geopy.exc import GeocoderUnavailable
from requests.exceptions import ConnectionError
import requests
from .decorator import delivery_guy_required
from geopy.geocoders import Nominatim
from django.conf import settings
from django.templatetags.static import static
from django.contrib import messages
from math import radians, sin, cos, sqrt, atan2


@delivery_guy_required
def assiged_delivery(request):
    if request.method == 'POST':
        current_user = request.user
        delivery_order = request.POST.get('order')
        order = Delivery.objects.get(
            delivery_person__user__email=current_user, order__order_number=delivery_order)

        order.status = 'InProgress'
        order.save()
        return redirect('current_delivery')
    else:
        current_user = request.user
        user = DeliveryGuy.objects.get(user__email=current_user)
        status = user.status
        deliverys = Delivery.objects.filter(
            delivery_person__user__email=current_user, status="Recived")
        if not deliverys:
            return render(request, 'delivery_person/assigned_delivery.html')
        else:
            try:
                current_user = request.user
                user = DeliveryGuy.objects.get(user__email=current_user)
                status = user.status
                deliverys = Delivery.objects.filter(
                    delivery_person__user__email=current_user, status="Recived")
                # delivery location
                dest_latitude = None
                dest_longitude = None

                for delivery in deliverys:
                    dest_latitude = delivery.order.latitude
                    dest_longitude = delivery.order.longitude
                    geolocator = Nominatim(user_agent="Engebeyay")
                    location = geolocator.reverse(
                        f"{dest_latitude}, {dest_longitude}", addressdetails=True)

                # Check if delivery is already accepted
                deliveries = Delivery.objects.filter(
                    delivery_person__user__email=current_user, status="InProgress")
                exist = deliveries.exists()
                context = {'deliverys': deliverys,
                           'status': status,
                           'location': location,
                           'exist': exist}
                return render(request, 'delivery_person/assigned_delivery.html', context)
            except Exception as e:
                error_message = "An error occurred. Please check your connection or try again later."
                context = {"error_message": error_message}
                return render(request, "delivery_person/error.html", context)


@delivery_guy_required
def current_delivery(request):
    current_user = request.user
    deliverys = Delivery.objects.filter(
        delivery_person__user__email=current_user, status="InProgress")

    if not deliverys:
        return render(request, 'delivery_person/current_delivery.html')
    else:
        try:
            # current_user = request.user
            # deliverys = Delivery.objects.filter(
            # delivery_person__user__email=current_user, status="InProgress")
            # Retrieve the latitude and longitude for the destination (buyer's location)
            dest_latitude = None
            dest_longitude = None
            order_num = None

            for delivery in deliverys:
                order_num = delivery.order.order_number
                dest_latitude = delivery.order.latitude
                dest_longitude = delivery.order.longitude
            try:
                geolocator = Nominatim(user_agent="Engebeyay")
                location = geolocator.reverse(
                    f"{dest_latitude}, {dest_longitude}")
            except GeocoderUnavailable:
                location = "Geocoding service is currently unavailable."

            # Retrieve the latitude and longitude for all the sellers' locations
            ordered_items = OrderedProduct.objects.filter(
                order__order_number=order_num)
            processed_owners = set()
            latitude_list = []
            longitude_list = []

            for ordered_item in ordered_items:
                owner = ordered_item.product.owner

                if owner not in processed_owners:
                    # Retrieve latitude and longitude only for unique owners
                    latitude = owner.latitude
                    longitude = owner.longitude

                    # Add the latitude and longitude values to the lists
                    latitude_list.append(latitude)
                    longitude_list.append(longitude)

                    # Add the owner to the set of processed owners
                    processed_owners.add(owner)
            # Add the buyer's location at the end!
            latitude_list.append(dest_latitude)
            longitude_list.append(dest_longitude)

            # Set up the API endpoint and parameters
            url = "https://maps.googleapis.com/maps/api/directions/json"
            origin = f"{dest_latitude},{dest_longitude}"
            waypoints = "|".join(
                [f"{lat},{lng}" for lat, lng in zip(latitude_list, longitude_list)])
            destination = f"{latitude_list[-1]},{longitude_list[-1]}"
            api_key = settings.MAP_API_KEY
            params = {
                "origin": origin,
                "destination": destination,
                "waypoints": waypoints,
                "key": api_key
            }

            # Make a request to the API
            response = requests.get(url, params=params)
            data = json.loads(response.text)

            # Extract the route coordinates from the response
            polyline = data["routes"][0]["overview_polyline"]["points"]
            route_coordinates = decode_polyline(polyline)
            markers = []

            buyer_marker = {
                "latitude": dest_latitude,
                "longitude": dest_longitude,
                "icon": {
                    "url": static('icons/finish.png'),
                    "scaledSize": [40, 40]
                }
            }

            # Iterate over latitude_list and longitude_list
            for lat, lng in zip(latitude_list, longitude_list):
                # Check if the current marker is at the same location as the buyer marker
                if lat == buyer_marker["latitude"] and lng == buyer_marker["longitude"]:
                    continue  # Skip this marker and move to the next iteration

                markers.append({
                    "latitude": lat,
                    "longitude": lng,
                    "icon": {
                        "url": static('icons/location2.png'),
                        "scaledSize": [40, 40]
                    }
                })

            markers.append(buyer_marker)

            distance = 0.0
            # Calculate the distance between consecutive locations
            for i in range(len(latitude_list) - 1):
                start_location = (latitude_list[i], longitude_list[i])
                end_location = (latitude_list[i + 1], longitude_list[i + 1])
                distance += calculate_distance(start_location, end_location)

            distance = round(distance, 2)

            context = {
                "route_coordinates": route_coordinates,
                "location": location,
                "deliverys": deliverys,
                "map_api_key": api_key,
                "markers": markers,
                "min_covered_distance": distance
            }

            return render(request, 'delivery_person/current_delivery.html', context)
        except Exception as e:
            error_message = "An error occurred. Please check your connection or try again later."
            context = {"error_message": error_message}
            return render(request, "delivery_person/error.html", context)


def decode_polyline(polyline):
    coordinates = []
    index = 0
    lat = 0
    lng = 0

    while index < len(polyline):
        shift = 0
        result = 0

        while True:
            byte = ord(polyline[index]) - 63
            index += 1
            result |= (byte & 0x1F) << shift
            shift += 5
            if byte < 0x20:
                break

        dlat = ~(result >> 1) if result & 1 else result >> 1
        lat += dlat

        shift = 0
        result = 0

        while True:
            byte = ord(polyline[index]) - 63
            index += 1
            result |= (byte & 0x1F) << shift
            shift += 5
            if byte < 0x20:
                break

        dlng = ~(result >> 1) if result & 1 else result >> 1
        lng += dlng

        coordinates.append((lat * 1e-5, lng * 1e-5))

    return coordinates


# Draw The Route
def decode_polyline(polyline):
    index = 0
    coordinates = []
    lat = 0
    lng = 0

    while index < len(polyline):
        shift = 0
        result = 0

        while True:
            byte = ord(polyline[index]) - 63
            index += 1
            result |= (byte & 0x1F) << shift
            shift += 5
            if byte < 0x20:
                break

        dlat = ~(result >> 1) if result & 1 else result >> 1
        lat += dlat

        shift = 0
        result = 0

        while True:
            byte = ord(polyline[index]) - 63
            index += 1
            result |= (byte & 0x1F) << shift
            shift += 5
            if byte < 0x20:
                break

        dlng = ~(result >> 1) if result & 1 else result >> 1
        lng += dlng

        coordinates.append((lat * 1e-5, lng * 1e-5))

    return coordinates


# Calculate the Distance
def calculate_distance(start_location, end_location):
    # Radius of the Earth in kilometers
    earth_radius = 6371.0

    lat1, lon1 = map(radians, start_location)
    lat2, lon2 = map(radians, end_location)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = earth_radius * c
    return distance


@delivery_guy_required
def confirm_delivery(request):

    if request.method == 'POST':
        current_user = request.user
        json_data = json.loads(request.body)
        result = json_data.get('result')
        distance = json_data.get('distance')
        print(result)
        # update delivery model
        delivery = Delivery.objects.get(
            delivery_person__user__email=current_user, order__order_number=result)
        delivery.status = 'Completed'
        delivery.save()
        # update order model
        order = Order.objects.get(order_number=result)
        order.status = 'Delivred'
        order.save()

    # update delivery guy
        delivery_guy = DeliveryGuy.objects.get(user__email=current_user)
        fee = float(delivery_guy.company.delivery_fee)
        price = fee * float(distance)
        delivery_guy.driven += float(distance)
        delivery_guy.earnings += price
        delivery_guy.completed_jobs += 1
        delivery_guy.save()

    return redirect('delivery_profile')


@delivery_guy_required
def delivery_profile(request):
    if request.method == 'POST':
        current_user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        p_number = request.POST.get('phone_number')
        check = request.POST.get('status')

        if check == 'on':
            status = "Active"
        else:
            status = "InActive"

        user = DeliveryGuy.objects.get(user__email=current_user)
        # update delivery person profile
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = p_number
        user.status = status
        user.save()
        messages.success(request, 'Profile Updated Sucessfuly.')
        return redirect('delivery_profile')
    else:
        current_user = request.user
        user = DeliveryGuy.objects.get(user__email=current_user)
        context = {
            "user": user,
        }
        return render(request, 'delivery_person/delivery_profile.html', context)


@delivery_guy_required
def delivery_guy_change_password(request):

    delivery = DeliveryGuy.objects.get(user=request.user)

    if request.POST['password'] == request.POST['confirm_password']:
        delivery.user.set_password(request.POST['password'])
        delivery.user.save()
        messages.success(request, 'Password changed successfully.')
        return redirect('login')
    else:
        messages.error(request, 'Please try again.')
        return redirect('delivery_profile')
