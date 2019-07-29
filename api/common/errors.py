""" Exception errors."""

from flask import jsonify


class NotFound():
    def response(self, entity, id):
        """return Not found message."""
        data = {
            "status": "Failure",
            "message": "{} with id {} Not found".format(entity, id)
                }
        return jsonify(data), 404
