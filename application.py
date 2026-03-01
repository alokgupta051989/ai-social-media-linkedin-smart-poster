from backend.main import app

# Elastic Beanstalk expects 'application' variable
application = app

if __name__ == "__main__":
    application.run(debug=True)