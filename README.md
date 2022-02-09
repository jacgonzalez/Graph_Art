# Art creation through the use of graphs
Data structures project. Creates a graph structure from a base stippled image.

This project uses code from the following projects:
* PyTSPArt: https://github.com/RoboTums/PyTSPArt
* The presentation of this project is inside this link: https://docs.google.com/presentation/d/1hgaiHGW1DUUE1qAda9O07la-UbRinc-C6Axa5ylRVpY/edit#slide=id.g107664ea9c0_0_4

## Steps to use the interface
To follow these steps use a virtualenv if desired (Not required).
* Open the console and move to the project directory.
* Install all the requirements `pip install -r requirements.txt`.
* Move to src folder on the console and run `uvicorn api:app  --reload --host 0.0.0.0 --port 8000`. Do not close the console so the Api keeps running.
* Open `index.html` on the root folder of the project and use the interface.