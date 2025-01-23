# Project I made in the first year of University
## Link to Video Which Runs the Code: **https://www.youtube.com/watch?v=cqJ_Y9t2Kyk**

## Setting Up a Virtual Environment

### **Windows**
1. Open a terminal or command prompt.
2. Navigate to project directory:
   ```bash
   cd AsteroidsGame
3. Create a Virtual Environment:
    ```bash
    python -m venv venv
4. Activate the Virtual Environment
    ```bash
    venv/Scripts/activate

### **macOS/Linux**
1. Open a terminal or command prompt.
2. Navigate to project directory:
    ```bash
    cd AsteroidsGame
3. Create a Virtual Environment
    ```bash
    python3 -m venv venv
4. Activate the Virtual Environment
    ```bash
    source venv/bin/activate

## Installing Required Dependencies
1. Ensuring the virtual environment is activated.
2. Ensure you are in the same directory as requirements.txt
3. Run the Command:
    ```bash
    pip install -r requirements.txt
4. The venv should be running with the libraries in requirements.txt installed
5. Once finished, to exist the Virtual Environment type:
    ```bash
    deactivate
## Running the Software
In the terminal/command line run:
1. Play the game by running:
    ```bash
    python Asteroid.py