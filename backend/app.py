from setup import *

@app.route('/')
def index():
    all_issuers = issuers.query.all()
    return str(all_issuers)

#this is the main function that runs the app
if __name__ == '__main__':
    app.run(debug = True)