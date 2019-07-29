"""Application Utility Functions."""

import datetime
import uuid

FORMAT = "%d-%m-%Y %H:%M:%S"


def generate_id():
    return str(uuid.uuid4())


def time_utility():
    """Function to generate and return current time in favourable format."""
    current_time = datetime.datetime.now()
    return current_time
    # return current_time.strftime(FORMAT)


def validate_entity(entity, entity_name):
        """utility function for validating various entities."""
        if not entity:
            raise AssertionError("No {} provided".format(entity_name))
        if entity.split() == []:
            raise AssertionError("{} cannot be an empty string".format(
                entity_name
                )
            )
        if set(r'[~!@#$%^&*()_+{}":;\']+$').intersection(entity):
            raise AssertionError("{} cannot contain special characters".format(
                entity_name
                )
            )
        return entity
