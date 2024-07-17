from pathlib import Path
import pandas as pd
import seaborn as sns
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from joblib import load
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

sns.set_theme(style="white")

base_path = Path(__file__).parent
scaler = load(base_path / "models" / "scaler.joblib")
knn = load(base_path / "models" / "knn_model.joblib")
data = pd.read_csv(base_path / "data" / "cleaned_data.csv")


page_a_content = ui.page_fluid(
    ui.card(
        ui.card_header(
            ui.HTML("""<h1>Explore the constellations of our universe! 🌌</h1>""")),
        ui.HTML("""
            <p>Welcome to the interactive constellation explorer! This tool lets you modify data attributes to discover stars of various constellations. </p>
                        <ul>
                <li><strong>Right Ascension:</strong> The celestial equivalent of longitude, RA measures how far east an object is from the celestial prime meridian in hours. </li>
                <li><strong>Declination:</strong> Similar to latitude on Earth, declination measures how far north or south an object is from the celestial equator in degrees</li>
                <li><strong>Apparent Magnitude:</strong> A measure of a star's brightness as seen from Earth; the lower the number, the brighter the star.</li>
                <li><strong>Absolute Magnitude:</strong> The brightness a star would have if it were located 10 parsecs (about 32.6 light years) away from Earth.</li>
                <li><strong>Distance from Earth:</strong> The actual distance between Earth and the star, measured in light years.</li>
            </ul>
            <h5><u>How It Works:</u></h5>
            <ul>
                <li><strong>Modify Star Attributes:</strong> Use intuitive sliders to adjust the Right Ascension, Declination, Apparent Magnitude, Absolute Magnitude, and Distance from Earth of stars.</li>
                <li><strong>Discover Constellations:</strong> As you modify the attributes, the tool dynamically calculates and displays the total number of stars matching your criteria, identifies the most significant constellation, and calculates the average distance of these stars from Earth.</li>
                <li><strong>Visualization and Analysis:</strong> View a plot that shows the number of stars per constellation and a detailed table listing all stars that match your specified criteria.</li>
            </ul>
            """)
    ),

    ui.layout_sidebar(ui.sidebar(
        ui.card(
            ui.card_header("Instructions"),
            ui.p(
                "❗Scroll up for definitions of data attributes! Default values are IQ range."),

        ),
        ui.p("      "),
        ui.input_slider(
            "ra",
            "Right Ascension",
            round(data['right_ascension'].min(), 2),
            round(data['right_ascension'].max(), 2),
            [round(data['right_ascension'].quantile(0.25), 2),
             round(data['right_ascension'].quantile(0.75), 2)],
        ),
        ui.input_slider(
            "dec",
            "Declination",
            round(data['declination'].min(), 2),
            round(data['declination'].max(), 2),
            [round(data['declination'].quantile(0.25), 2),
             round(data['declination'].quantile(0.75), 2)],
        ),
        ui.input_slider(
            "appmag",
            "Apparent Magnitude",
            round(data['apparent_magnitude'].min(), 2),
            round(data['apparent_magnitude'].max(), 2),
            [round(data['apparent_magnitude'].quantile(0.25), 2),
             round(data['apparent_magnitude'].quantile(0.75), 2)],
        ),
        ui.input_slider(
            "absmag",
            "Absolute Magnitude",
            round(data['absolute_magnitude'].min(), 2),
            round(data['absolute_magnitude'].max(), 2),
            [round(data['absolute_magnitude'].quantile(0.25), 2),
             round(data['absolute_magnitude'].quantile(0.75), 2)],
        ),
        ui.input_slider(
            "dist",
            "Distance",
            round(data['distance_light_year'].min(), 2),
            round(data['distance_light_year'].max(), 2),
            [round(data['distance_light_year'].quantile(0.25), 2),
             round(data['distance_light_year'].quantile(0.75), 2)],
        ),

    ),
        ui.layout_column_wrap(
            ui.value_box(
                "Total Stars",
                ui.output_text("total_stars"),
                "The total number of stars meeting all input criteria",
                theme="primary",
            ),
            ui.value_box(
                "Most Significant Constellation",
                ui.output_text("most_significant_constellation"),
                "Constellation with the most stars from the input criteria.",
                theme="primary",
            ),
            ui.value_box(
                "Average Distance",
                ui.output_text("average_distance"),
                "Average distance of stars from Earth meeting input criteria.",
                theme="primary",
            )
    ),

        ui.card(
        ui.card_header("Constellation Plot"),
        ui.output_plot("constplot"),
    ),
        ui.card(
        ui.card_header("Statistical Data"),
        ui.output_data_frame("constdata"),
    )
    )
)


page_b_content = ui.page_fluid(
    ui.card(
        ui.card_header(
            ui.HTML("""<h1>Explore the stars of our universe 💫</h1>""")),
        ui.HTML("""
            <p>Explore and compare data attributes of stars within constellations using our interactive Star Explorer tool. </p>
                        <ul>
                <li><strong>Right Ascension:</strong> The celestial equivalent of longitude, RA measures how far east an object is from the celestial prime meridian in hours. </li>
                <li><strong>Declination:</strong> Similar to latitude on Earth, declination measures how far north or south an object is from the celestial equator in degrees</li>
                <li><strong>Apparent Magnitude:</strong> A measure of a star's brightness as seen from Earth; the lower the number, the brighter the star.</li>
                <li><strong>Absolute Magnitude:</strong> The brightness a star would have if it were located 10 parsecs (about 32.6 light years) away from Earth.</li>
                <li><strong>Distance from Earth:</strong> The actual distance between Earth and the star, measured in light years.</li>
            </ul>
            <h5><u>How It Works:</u></h5>
            <ul>
                <li><strong>Select a Constellation:</strong> Begin by choosing a constellation from a dropdown menu. This action will populate a scatter plot with all the stars within the chosen constellation, including display the average values.</li>
                <li><strong>View Stars:</strong> Select stars which are part of the constellation for comparison (This feature will be added in the future!)</li>
                <li><strong>Dynamic Visualization:</strong> The tool automatically updates to display five different scatter plots, each illustrating various attributes of the stars such as Right Ascension, Declination, Apparent Magnitude, and Absolute Magnitude.</li>
            </ul>
            """)
    ),

    ui.layout_sidebar(ui.sidebar(
        ui.card(
            "❗Not all constellations have star data (see About) and as a result, will not produce a plot"
        ),
        ui.input_selectize(
            "constellation_select",
            "Select a Constellation:",
            choices={
                "Andromeda": "Andromeda", "Antlia": "Antlia", "Apus": "Apus", "Aquarius": "Aquarius",
                "Aquila": "Aquila", "Ara": "Ara", "Aries": "Aries", "Auriga": "Auriga",
                "Boötes": "Boötes", "Caelum": "Caelum", "Camelopardalis": "Camelopardalis", "Cancer": "Cancer",
                "Canes Venatici": "Canes Venatici", "Canis Major": "Canis Major", "Canis Minor": "Canis Minor",
                "Capricornus": "Capricornus", "Carina": "Carina", "Cassiopeia": "Cassiopeia", "Centaurus": "Centaurus",
                "Cepheus": "Cepheus", "Cetus": "Cetus", "Chamaeleon": "Chamaeleon", "Circinus": "Circinus",
                "Columba": "Columba", "Coma Berenices": "Coma Berenices", "Corona Australis": "Corona Australis",
                "Corona Borealis": "Corona Borealis", "Corvus": "Corvus", "Crater": "Crater", "Crux": "Crux",
                "Cygnus": "Cygnus", "Delphinus": "Delphinus", "Dorado": "Dorado", "Draco": "Draco",
                "Equuleus": "Equuleus", "Eridanus": "Eridanus", "Fornax": "Fornax", "Gemini": "Gemini",
                "Grus": "Grus", "Hercules": "Hercules", "Horologium": "Horologium", "Hydra": "Hydra",
                "Hydrus": "Hydrus", "Indus": "Indus", "Lacerta": "Lacerta", "Leo": "Leo", "Leo Minor": "Leo Minor",
                "Lepus": "Lepus", "Libra": "Libra", "Lupus": "Lupus", "Lynx": "Lynx", "Lyra": "Lyra",
                "Mensa": "Mensa", "Microscopium": "Microscopium", "Monoceros": "Monoceros", "Musca": "Musca",
                "Norma": "Norma", "Octans": "Octans", "Ophiuchus": "Ophiuchus", "Orion": "Orion",
                "Pavo": "Pavo", "Pegasus": "Pegasus", "Perseus": "Perseus", "Phoenix": "Phoenix",
                "Pictor": "Pictor", "Pisces": "Pisces", "Piscis Austrinus": "Piscis Austrinus",
                "Puppis": "Puppis", "Pyxis": "Pyxis", "Reticulum": "Reticulum", "Sagitta": "Sagitta",
                "Sagittarius": "Sagittarius", "Scorpius": "Scorpius", "Sculptor": "Sculptor", "Scutum": "Scutum",
                "Serpens": "Serpens", "Sextans": "Sextans", "Taurus": "Taurus", "Telescopium": "Telescopium",
                "Triangulum": "Triangulum", "Triangulum Australe": "Triangulum Australe", "Tucana": "Tucana",
                "Ursa Major": "Ursa Major", "Ursa Minor": "Ursa Minor", "Vela": "Vela", "Virgo": "Virgo",
                "Volans": "Volans", "Vulpecula": "Vulpecula"
            },
        ),
        ui.card(
            "❗ Many of the star names contain greek characters."
        ),
        ui.output_ui('star_select'),
    ),

        ui.layout_columns(
            ui.card(
                ui.card_header("Right Ascension"),
                ui.output_plot("sra"),
            ),
            ui.card(
                ui.card_header("Declination"),
                ui.output_plot("sdec"),
            ),

    ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Apparent Magnitude"),
                ui.output_plot("sappmag"),
            ),
            ui.card(
                ui.card_header("Absolute Magnitude"),
                ui.output_plot("sabsmag"),
            ),

    ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Distance (light years)"),
                ui.output_plot("sdist"),
            ),
    ),
    )
)

page_c_content = ui.page_fluid(
    ui.card(
        ui.card_header(ui.HTML("""<h1>Predict your own star! 🌠</h1>""")),
        ui.HTML("""
                <p>This interactive tool allows you to explore the cosmos by entering a star name of your choice and adjusting its right ascension and declination using intuitive sliders. Once you submit your entry, our model predicts which constellation your star is likely part of.</p>
                <h5><u>How It Works:</u></h5>
                <ul>
                    <li><strong>Enter a Star Name:</strong> Choose a name for your star. It can be real or fictional!</li>
                    <li><strong>Set Coordinates:</strong> Use the sliders to specify the right ascension (0 to 24 hours) and declination (-90 to 90 degrees) of your star.</li>
                    <li><strong>Predict Constellation:</strong> Click 'Submit' to see the predicted constellation based on your inputs.</li>
                </ul>
                <h5><u>Behind the Scenes:</u></h5>
                <p>The model employs the K-Nearest Neighbors (KNN) machine learning algorithm, a simple yet powerful method used widely in classification tasks. KNN works by finding the closest training examples in the feature space and making predictions based on their classifications. This model was trained on a dataset of 3,994 records and achieved a 94% accuracy on the test set.</p>
            """)
    ),
    ui.layout_columns(
        ui.card(
            ui.card_header("Enter Star Name"),
            ui.input_text("star_name", "Star Name", ""),
        ),
        ui.card(
            ui.card_header("Set Coordinates"),
            ui.input_slider("right_ascension", "Right Ascension", 0, 24, 12),
            ui.input_slider("declination", "Declination", -90, 90, 0)
        )
    ),
    ui.card(
        ui.input_action_button("submit", "Submit", class_="btn-success"),
        class_="justify-content-center text-center"
    ),
    ui.output_ui("text"),
)

page_d_content = ui.page_fluid(
    ui.card(
        ui.card_header(
            ui.HTML("""<h1>Celestial Insights by Serena Gong</h1>""")),
        ui.markdown("""
                <p>Celestial Insights is an interactive web application made using Shiny by Python designed to provide educational insights into constellations using data-driven methods. There are 3 features, comparison of stars across constellations, stars within constellations, and predicting a star's constellation. This part allows users to input data about stars and utilizes a machine learning model to predict which constellation a given star might belong to based on its celestial coordinates.</p>
                <h5><u>Data Source:</u></h5>
                <p>The star data used in this application is sourced from <a href="https://api-ninjas.com/api/stars" target="_blank"> Ninjas API</a>. The API provides comprehensive and accurate astronomical data, which is essential for our application's functionality. Please note that the API source only supplies data for 3994 stars, which is what is used for this application. There obviously exists more stars in our universe!</p>
                <h5><u>Context:</u></h5>
                <p>Stars have fascinated humanity for millennia! This application is intended for educational purposes in the field of astronomy. It can be used by educators in classroom settings, students for learning and projects, and amateur astronomers or anyone interested in learning more about the stars and constellations. The interactive features allow users to explore celestial data visually, making complex information more digestible and interesting.</p>
                <h5><u>Usage Instructions:</u></h5>
                <p>Visit each page individually for usage instructions.</p>
            """)
    ),
)

app_ui = ui.page_navbar(
    ui.nav_panel("Constellations", page_a_content),
    ui.nav_panel("Stars", page_b_content),
    ui.nav_panel("Prediction", page_c_content),
    ui.nav_panel("About", page_d_content),
    title="Celestial Insights ⭐",
    id="page",
    footer=ui.div(
        {
            "style": "width:100%; padding: 5px 0; text-align: center; border-top: 2px solid black;"
        },
        ui.tags.style(
            """
            h4 {
                color: black; 
            }
            .footer-text {
                font-size: 14px;
                color: black; 
            }
            """
        ),
        ui.h4("✩₊˚.⋆☾⋆⁺₊", {
              "style": "margin-top: 0.3em; margin-bottom: 0.3em;"}),
        ui.p("Made by Serena Gong", {
             "class": "footer-text"})
    )
)


def server(input: Inputs, output: Outputs, session: Session):
    @render.plot
    @reactive.event(input.constellation_select)
    def sra():
        constellation = input.constellation_select()
        if constellation:
            filtered_data = data[data['constellation'] == constellation]
            avg_declination = filtered_data['right_ascension'].mean()

            plt.figure(figsize=(10, 5))
            sns.stripplot(x='right_ascension', data=filtered_data,
                          jitter=True, size=3)

            plt.title('Right Ascension of stars in ' + constellation)
            plt.xlabel('Right Ascension (hour)')
            plt.grid()

            plt.axvline(avg_declination, color='red', linestyle='--',
                        label=f'Average Right Ascension: {avg_declination:.2f}')
            plt.legend()

            return plt.gcf()

    @render.plot
    @reactive.event(input.constellation_select)
    def sdec():
        constellation = input.constellation_select()
        if constellation:
            filtered_data = data[data['constellation'] == constellation]
            avg_declination = filtered_data['declination'].mean()

            plt.figure(figsize=(10, 5))
            sns.stripplot(x='declination', data=filtered_data,
                          jitter=True, size=3)

            plt.title('Declination of stars in ' + constellation)
            plt.xlabel('Declination (degrees)')
            plt.grid()

            plt.axvline(avg_declination, color='red', linestyle='--',
                        label=f'Average Declination: {avg_declination:.2f}')
            plt.legend()

            return plt.gcf()

    @render.plot
    @reactive.event(input.constellation_select)
    def sabsmag():
        constellation = input.constellation_select()
        if constellation:
            filtered_data = data[data['constellation'] == constellation]
            avg_declination = filtered_data['absolute_magnitude'].mean()

            plt.figure(figsize=(10, 5))
            sns.stripplot(x='absolute_magnitude',
                          data=filtered_data, jitter=True, size=3)
            plt.title('Absolute Magnitude of stars in ' + constellation)
            plt.xlabel('Absolute Magnitude')
            plt.grid()
            plt.axvline(avg_declination, color='red', linestyle='--',
                        label=f'Average Absolute Magnitude: {avg_declination:.2f}')
            plt.legend()
            return plt.gcf()

    @render.plot
    @reactive.event(input.constellation_select)
    def sappmag():
        constellation = input.constellation_select()
        if constellation:
            filtered_data = data[data['constellation'] == constellation]
            avg_declination = filtered_data['apparent_magnitude'].mean()

            plt.figure(figsize=(10, 5))
            sns.stripplot(x='apparent_magnitude',
                          data=filtered_data, jitter=True, size=3)
            plt.title('Apparent Magnitude of stars in ' + constellation)
            plt.xlabel('Apparent Magnitude')
            plt.grid()
            plt.axvline(avg_declination, color='red', linestyle='--',
                        label=f'Average Apparent Magnitude: {avg_declination:.2f}')
            plt.legend()
            return plt.gcf()

    @render.plot
    @reactive.event(input.constellation_select)
    def sdist():
        constellation = input.constellation_select()
        if constellation:
            filtered_data = data[data['constellation'] == constellation]
            avg_declination = filtered_data['distance_light_year'].mean()

            plt.figure(figsize=(10, 5))
            sns.stripplot(x='distance_light_year',
                          data=filtered_data, jitter=True, size=3)
            plt.title('Distance from Earth of stars in ' + constellation)
            plt.xlabel('Distance from Earth (light years)')
            plt.grid()
            plt.axvline(avg_declination, color='red', linestyle='--',
                        label=f'Average Distance from Earth: {avg_declination:.2f} light years')
            plt.legend()
            return plt.gcf()

    def get_stars():
        constellation = input.constellation_select()
        if constellation:
            filtered_data = data[data['constellation'] == constellation]
            return {row: row for row in filtered_data['name'].unique()}
        else:
            return {}

    @render.ui
    def star_select():
        stars = get_stars()
        return (ui.input_selectize("selectize", "Stars in Constellation: ", choices=stars, multiple=True))

    @render.text
    @reactive.event(input.ra, input.dec, input.appmag, input.absmag, input.dist)
    def total_stars():
        ra_range = input.ra()
        dec_range = input.dec()
        appmag_range = input.appmag()
        absmag_range = input.absmag()
        dist_range = input.dist()

        filtered_data = data[
            (data['right_ascension'].between(*ra_range)) &
            (data['declination'].between(*dec_range)) &
            (data['apparent_magnitude'].between(*appmag_range)) &
            (data['absolute_magnitude'].between(*absmag_range)) &
            (data['distance_light_year'].between(*dist_range))
        ]
        total_stars = len(filtered_data)
        return total_stars

    @render.text
    @reactive.event(input.ra, input.dec, input.appmag, input.absmag, input.dist)
    def most_significant_constellation():
        ra_range = input.ra()
        dec_range = input.dec()
        appmag_range = input.appmag()
        absmag_range = input.absmag()
        dist_range = input.dist()

        filtered_data = data[
            (data['right_ascension'].between(*ra_range)) &
            (data['declination'].between(*dec_range)) &
            (data['apparent_magnitude'].between(*appmag_range)) &
            (data['absolute_magnitude'].between(*absmag_range)) &
            (data['distance_light_year'].between(*dist_range))
        ]
        if not filtered_data.empty:
            constellation_counts = filtered_data['constellation'].value_counts(
            )
            most_significant_constellation = constellation_counts.idxmax()
            count_in_constellation = constellation_counts[most_significant_constellation]
            return f"{most_significant_constellation} ({count_in_constellation})"
        else:
            return "N/A"

    @render.text
    @reactive.event(input.ra, input.dec, input.appmag, input.absmag, input.dist)
    def average_distance():
        ra_range = input.ra()
        dec_range = input.dec()
        appmag_range = input.appmag()
        absmag_range = input.absmag()
        dist_range = input.dist()

        filtered_data = data[
            (data['right_ascension'].between(*ra_range)) &
            (data['declination'].between(*dec_range)) &
            (data['apparent_magnitude'].between(*appmag_range)) &
            (data['absolute_magnitude'].between(*absmag_range)) &
            (data['distance_light_year'].between(*dist_range))
        ]
        average_distance = round(filtered_data['distance_light_year'].mean(
        ), 2) if not filtered_data.empty else 0

        return f"{average_distance} light years"

    @render.plot
    @reactive.event(input.ra, input.dec, input.appmag, input.absmag, input.dist)
    def constplot():
        ra_range = input.ra()
        dec_range = input.dec()
        appmag_range = input.appmag()
        absmag_range = input.absmag()
        dist_range = input.dist()

        filtered_data = data[
            (data['right_ascension'].between(*ra_range)) &
            (data['declination'].between(*dec_range)) &
            (data['apparent_magnitude'].between(*appmag_range)) &
            (data['absolute_magnitude'].between(*absmag_range)) &
            (data['distance_light_year'].between(*dist_range))
        ]
        constellation_counts = filtered_data['constellation'].value_counts(
        ).reset_index()
        constellation_counts.columns = ['constellation', 'count']

        constellation_counts = constellation_counts[constellation_counts['count'] > 0]

        fig, ax = plt.subplots()

        barplot = sns.barplot(
            x='constellation', y='count', hue='constellation', data=constellation_counts, palette='viridis', legend=False
        )
        ax.set_title('Number of Stars per Constellation')
        ax.set_xlabel('Constellation')
        ax.set_ylabel('Number of Stars')
        max_count = constellation_counts['count'].max()
        ax.set_ylim(0, max_count * 1.1)

        ax.set_xticks(range(len(constellation_counts['constellation'])))
        ax.set_xticklabels(
            constellation_counts['constellation'], rotation=45, ha='right')

        plt.grid()
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.0f'),
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center',
                        xytext=(0, 5),
                        textcoords='offset points',
                        fontsize=9)
        return fig

    @render.data_frame
    def constdata():
        ra_range = input.ra()
        dec_range = input.dec()
        appmag_range = input.appmag()
        absmag_range = input.absmag()
        dist_range = input.dist()

        filtered_data = data[
            (data['right_ascension'].between(*ra_range)) &
            (data['declination'].between(*dec_range)) &
            (data['apparent_magnitude'].between(*appmag_range)) &
            (data['absolute_magnitude'].between(*absmag_range)) &
            (data['distance_light_year'].between(*dist_range))
        ].copy()

        filtered_data['count'] = filtered_data.groupby(
            'constellation')['constellation'].transform('count')

        filtered_data = filtered_data.sort_values(by='count', ascending=False)
        filtered_data = filtered_data.drop(columns=['count'])

        filtered_data = filtered_data.rename(columns={
            'name': 'Star Name',
            'constellation': 'Constellation',
            'right_ascension': 'Right Ascension',
            'declination': 'Declination',
            'apparent_magnitude': 'Apparent Magnitude',
            'absolute_magnitude': 'Absolute Magnitude',
            'distance_light_year': 'Distance',
            'spectral_class': 'Spectral Class'
        })

        filtered_data.reset_index(drop=True, inplace=True)

        return render.DataGrid(filtered_data)

    @render.ui
    @reactive.event(input.submit, ignore_none=False)
    def text():
        star_name = input.star_name()
        ra = input.right_ascension()
        dec = input.declination()
        if star_name and (ra is not None) and (dec is not None):
            test_data = pd.DataFrame({
                'right_ascension': [ra],
                'declination': [dec]
            })
            test_features = scaler.transform(test_data)
            predictions = knn.predict(test_features)
            prediction_prob = knn.predict_proba(test_features)[0]

            class_probabilities = {}
            for idx, prob in enumerate(prediction_prob):
                if prob > 0.05:
                    class_probabilities[knn.classes_[idx]] = prob

            result_text = (
                f"<ul>"
                f"<li><b>Your star's name is:</b> {star_name}</li>"
                f"<li><b>Right ascension:</b> {ra}</li>"
                f"<li><b>Declination:</b> {dec}</li>"
                f"<li><b>Predicted Constellation:</b> {predictions[0]}</li>"
                f"<li><b>Probabilities of Predictions Constellation Breakdown:</b>"
                f"<ul>"
                + "".join(f"<li>{constellation}: {prob*100:.2f}%</li>" for constellation,
                          prob in class_probabilities.items())
                + f"</ul></li></ul>"
            )
            return (ui.card(
                ui.card_header("Results"),
                ui.HTML(result_text)

            ))


def count_species(df, species):
    return df[df["Species"] == species].shape[0]


app = App(app_ui, server)
if __name__ == "__main__":
    app.run()
