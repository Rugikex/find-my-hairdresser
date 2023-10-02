import random
import os

from dotenv import load_dotenv
from geopy.distance import great_circle
import googlemaps


load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    print("Please set the GOOGLE_API_KEY environment variable.")
    exit(1)


def get_valid_rating() -> float:
    """
    Asks the user for a valid rating between 0.0 and 5.0.

    :return: The valid rating.
    :rtype: float
    """
    while True:
        min_rating_str = input("Enter the minimum rating (0.0 - 5.0): ")
        try:
            min_rating = float(min_rating_str)
            if 0.0 <= min_rating <= 5.0:
                return min_rating
            else:
                print("Please enter a valid rating between 0.0 and 5.0.")
        except ValueError:
            print("Please enter a valid number.")


def get_valid_radius() -> int:
    """
    Asks the user for a valid radius between 0 and 50000.

    :return: The valid radius.
    :rtype: int
    """
    while True:
        radius_str = input("Enter the radius (in meters): ")
        try:
            radius = int(radius_str)
            if 0 <= radius <= 50_000:
                return radius
            else:
                print("Please enter a valid radius.")
        except ValueError:
            print("Please enter a valid number.")


def want_to_see_next_salon() -> bool:
    """
    Asks the user if they want to see the next salon.

    :return: True if the user wants to see the next salon, False otherwise.
    :rtype: bool
    """
    while True:
        choice = (
            input("\nDo you want to see the next salon? (yes/no): ").strip().lower()
        )
        if choice == "yes" or choice == "y":
            return True
        elif choice == "no" or choice == "n":
            return False
        else:
            print("Please enter a valid choice.")


def rating_to_stars(rating: float) -> str:
    """
    Converts a rating to a string of stars.

    :param rating: The rating to convert.
    :type rating: float

    :return: The string of stars.
    :rtype: str
    """
    stars = "★ " * int(rating)
    if rating - int(rating) >= 0.5:
        stars += "½"
    else:
        stars = stars.strip()
    return stars


def find_hair_salons() -> None:
    """
    Finds hair salons in a given area with a rating above a given minimum rating.

    :return: None
    :rtype: None
    """
    gmaps = googlemaps.Client(key=google_api_key)

    street = input("Enter the street (or area): ")
    city = input("Enter the city: ")
    country = input("Enter the country: ")
    min_rating = get_valid_rating()
    radius = get_valid_radius()

    location = f"{street}, {city}, {country}"

    geocode = gmaps.geocode(location)
    if not geocode:
        print(f"Location {location} not found.")
        return

    center_coords = geocode[0]["geometry"]["location"]
    center_point = (center_coords["lat"], center_coords["lng"])

    print(
        f"\nYour location: https://www.google.com/maps?q={center_point[0]},{center_point[1]} \
        \nSearching for hair salon with a rating of {min_rating} or higher on a radius of {radius} meters around your location..."
    )

    results = gmaps.places("coiffeur", location=location, radius=radius)

    if "results" in results:
        hair_salons = results["results"]

        filtered_salons = []
        for salon in hair_salons:
            place_details = gmaps.place(salon["place_id"])
            rating = place_details["result"].get("rating", 0.0)

            place_coords = place_details["result"]["geometry"]["location"]
            place_point = (place_coords["lat"], place_coords["lng"])

            distance = great_circle(center_point, place_point).meters

            if (
                rating >= min_rating
                and  distance <= radius
            ):
                formated_salon = {
                    "name": salon["name"],
                    "address": salon["formatted_address"],
                    "rating": rating,
                    "google_maps_link": place_details["result"]["url"],
                    "distance": f"{distance:.0f} meters",
                }
                filtered_salons.append(formated_salon)

        if not filtered_salons:
            print(
                f"\nNo hair salons with a rating of {min_rating} or higher were found in the {location} area."
            )
            return

        while filtered_salons:
            random_salon = random.choice(filtered_salons)
            name = random_salon.get("name", "Name not available")
            address = random_salon.get("address", "Address not available")
            rating = random_salon.get("rating", "Rating not available")
            google_maps_link = random_salon.get(
                "google_maps_link", "Google Maps link not available"
            )
            distance = random_salon.get("distance", "Distance not available")

            print(
                f"\nName: {name} \
                \nAddress: {address} \
                \nRating: {rating_to_stars(rating)} ({rating}) \
                \nGoogle Maps Link: {google_maps_link} \
                \nFlying distance: {distance}"
            )

            filtered_salons.remove(random_salon)

            if want_to_see_next_salon():
                continue
            break

        print(
            f"\nNo more hair salons with a rating of {min_rating} or higher were found in the {location} area."
        )

    else:
        print(f"No hair salons found in the {location} area.")


if __name__ == "__main__":
    find_hair_salons()
