# capstone_gradtrust
repository for segun-bake's capstone project: "Gradtrust"

## Python and Pip version
`python=3.12.0`
`pip=25.0.1`

## Automatic Debugging
create a .env file in the root directory with this line for automatic debugging:

```FLASK_DEBUG=1```

## Execute code
Run these commands in the terminal:

### Get all the dependencies
1. Create a virtual environment (name it whatever you want)
`python3 -m venv {name of virtual environment}`

2. Activate the virtual environment (for Mac/Linux/WSL)
`source {name of virtual environment}/bin/activate`

  if you are using Windows, use this command instead:

  `source {name of virtual environment}/Scripts/activate`

3. Install the dependencies
`pip install -r requirements.txt`

(Within the requirements.txt file, there are all the dependencies that are needed to run the application. Running the command above will install all these dependencies.)

### Run the application
Enter the following command in the terminal to run the application:
`flask run`

In the terminal, you should see a message that states the application is running on a local server. Copy the link and paste it into your browser to view the application.
