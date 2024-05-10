# CS498 Final Project (sxgong2)

## Statement of Purpose

Celestial Insights is an interactive web application designed to provide educational insights into constellations using data-driven methods. It offers three main features: comparison of stars across constellations, exploring stars within constellations, and predicting a star's constellation based on its celestial coordinates.

## Domain Context

Stars have fascinated humanity for millennia! This application is intended for educational purposes in the field of astronomy. It can be used by educators in classroom settings, students for learning and projects, amateur astronomers, or anyone interested in learning more about the stars and constellations. The interactive features allow users to explore celestial data visually, making complex information more digestible and interesting.

## Setup Instructions

1. **Clone the repository**:
    ```bash
    git clone https://github.com/illinois-cs-coursework/sp24_cs498e2e-final_sxgong2
    cd your-repo-directory
    ```

2. **Create a virtual environment**:
    ```bash
    python3.11 -m pip install uv
    uv venv
    source .venv/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    uv pip install -r requirements.txt
    ```

4. **Run the application**:
    ```bash
    python3 app.py run
    ```

## Usage Examples

### Feature 1: Comparison of Stars Across Constellations

Explore the constellations of our universe! This tool lets you modify data attributes to discover stars of various constellations.
- **Modify Star Attributes**: Use intuitive sliders to adjust the Right Ascension, Declination, Apparent Magnitude, Absolute Magnitude, and Distance from Earth of stars.
- **Discover Constellations**: As you modify the attributes, the tool dynamically calculates and displays the total number of stars matching your criteria, identifies the most significant constellation, and calculates the average distance of these stars from Earth.
- **Visualization and Analysis**: View a plot that shows the number of stars per constellation and a detailed table listing all stars that match your specified criteria.

### Feature 2: Exploring Stars Within Constellations

Explore and compare data attributes of stars within constellations using our interactive Star Explorer tool.
- **Select a Constellation**: Begin by choosing a constellation from a dropdown menu. This action will populate a scatter plot with all the stars within the chosen constellation, including display the average values.
- **View Stars**: Select stars which are part of the constellation for comparison (This feature will be added in the future!)
- **Dynamic Visualization**: The tool automatically updates to display five different scatter plots, each illustrating various attributes of the stars such as Right Ascension, Declination, Apparent Magnitude, and Absolute Magnitude.

### Feature 3: Predicting a Star's Constellation

Predict your own star! This interactive tool allows you to explore the cosmos by entering a star name of your choice and adjusting its right ascension and declination using intuitive sliders. Once you submit your entry, our model predicts which constellation your star is likely part of.
- **Enter a Star Name**: Choose a name for your star. It can be real or fictional!
- **Set Coordinates**: Use the sliders to specify the right ascension (0 to 24 hours) and declination (-90 to 90 degrees) of your star.
- **Predict Constellation**: Click 'Submit' to see the predicted constellation based on your inputs.

The model employs the K-Nearest Neighbors (KNN) machine learning algorithm, a simple yet powerful method used widely in classification tasks. KNN works by finding the closest training examples in the feature space and making predictions based on their classifications. This model was trained on a dataset of 3,994 records and achieved a 94% accuracy on the test set.

## Data Source

The star data used in this application is sourced from the [Ninjas API](https://api-ninjas.com/api/stars). The API provides comprehensive and accurate astronomical data, which is essential for our application's functionality. Please note that the API source only supplies data for 3994 stars, which is what is used for this application. There obviously exists more stars in our universe!
