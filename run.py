"""Run the flask Application."""

from api import app


if __name__ == "__main__":
    # run application
    app.run(host='0.0.0.0', port=5000, debug=True)
