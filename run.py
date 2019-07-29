"""Run the flask Application."""

from api import app


if __name__ == "__main__":
    # run application
    app.run(debug=True)
