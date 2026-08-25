from .models import CarMake, CarModel


def initiate():
    car_make_data = [
        {
            "name": "NISSAN",
            "description": "Great cars. Japanese technology"
        },
        {
            "name": "Mercedes",
            "description": "Great cars. German technology"
        },
        {
            "name": "Audi",
            "description": "Great cars. German technology"
        },
        {
            "name": "Kia",
            "description": "Great cars. Korean technology"
        },
        {
            "name": "Toyota",
            "description": "Great cars. Japanese technology"
        },
    ]

    # Create CarMake instances
    car_make_instances = []

    for data in car_make_data:
        car_make_instances.append(
            CarMake.objects.create(
                name=data["name"],
                description=data["description"]
            )
        )

    # Create 15 CarModel instances:
    # 3 models for each of the 5 makes.
    car_model_data = [
        # Nissan
        {
            "name": "Pathfinder",
            "type": "SUV",
            "year": 2023,
            "dealer_id": 1,
            "car_make": car_make_instances[0]
        },
        {
            "name": "Qashqai",
            "type": "SUV",
            "year": 2023,
            "dealer_id": 1,
            "car_make": car_make_instances[0]
        },
        {
            "name": "XTRAIL",
            "type": "SUV",
            "year": 2023,
            "dealer_id": 1,
            "car_make": car_make_instances[0]
        },

        # Mercedes
        {
            "name": "A-Class",
            "type": "SUV",
            "year": 2023,
            "dealer_id": 2,
            "car_make": car_make_instances[1]
        },
        {
            "name": "C-Class",
            "type": "SUV",
            "year": 2023,
            "dealer_id": 2,
            "car_make": car_make_instances[1]
        },
        {
            "name": "E-Class",
            "type": "SUV",
            "year": 2023,
            "dealer_id": 2,
            "car_make": car_make_instances[1]
        },

        # Audi
        {
            "name": "A4",
            "type": "SUV",
            "year": 2023,
            "dealer_id": 3,
            "car_make": car_make_instances[2]
        },
        {
            "name": "A5",
            "type": "SUV",
            "year": 2023,
            "dealer_id": 3,
            "car_make": car_make_instances[2]
        },
        {
            "name": "A6",
            "type": "SUV",
            "year": 2023,
            "dealer_id": 3,
            "car_make": car_make_instances[2]
        },

        # Kia
        {
            "name": "Sorrento",
            "type": "SUV",
            "year": 2023,
            "dealer_id": 4,
            "car_make": car_make_instances[3]
        },
        {
            "name": "Carnival",
            "type": "SUV",
            "year": 2023,
            "dealer_id": 4,
            "car_make": car_make_instances[3]
        },
        {
            "name": "Cerato",
            "type": "SEDAN",
            "year": 2023,
            "dealer_id": 4,
            "car_make": car_make_instances[3]
        },

        # Toyota
        {
            "name": "Corolla",
            "type": "SEDAN",
            "year": 2023,
            "dealer_id": 5,
            "car_make": car_make_instances[4]
        },
        {
            "name": "Camry",
            "type": "SEDAN",
            "year": 2023,
            "dealer_id": 5,
            "car_make": car_make_instances[4]
        },
        {
            "name": "Kluger",
            "type": "SUV",
            "year": 2023,
            "dealer_id": 5,
            "car_make": car_make_instances[4]
        },
    ]

    # Save CarModel instances
    for data in car_model_data:
        CarModel.objects.create(
            name=data["name"],
            car_make=data["car_make"],
            dealer_id=data["dealer_id"],
            type=data["type"],
            year=data["year"]
        )
