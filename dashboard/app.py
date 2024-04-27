from pathlib import Path
import pandas as pd
import seaborn as sns
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from joblib import load

sns.set_theme(style="white")
df = pd.read_csv(Path(__file__).parent / "penguins.csv", na_values="NA")
species = ["Adelie", "Gentoo", "Chinstrap"]

base_path = Path(__file__).parent.parent
scaler = load(base_path / "models" / "scaler.joblib")
knn = load(base_path / "models" / "knn_model.joblib")
data = pd.read_csv(base_path / "data" / "cleaned_data.csv")


min_right_ascension = data['right_ascension'].min()
max_right_ascension = data['right_ascension'].max()
min_declination = data['declination'].min()
max_declination = data['declination'].max()

print("Minimum Right Ascension:", min_right_ascension)
print("Maximum Right Ascension:", max_right_ascension)
print("Minimum Declination:", min_declination)
print("Maximum Declination:", max_declination)

def make_value_box(penguin):
    return ui.value_box(
        title=penguin, value=ui.output_text(f"{penguin}_count".lower()), theme="primary"
    )

page_a_content = ui.page_sidebar(
    ui.sidebar(
        ui.input_slider(
            "mass",
            "Mass",
            2000,
            6000,
            3400,
        ),
        ui.input_checkbox_group(
            "species", "Filter by species", species, selected=species
        ),
    ),
    ui.layout_columns(
        *[make_value_box(penguin) for penguin in species],
    ),
    ui.layout_columns(
        ui.card(
            ui.card_header("Summary statistics"),
            ui.output_data_frame("summary_statistics"),
        ),
        ui.card(
            ui.card_header("Penguin bills"),
            ui.output_plot("length_depth"),
        ),
    ),
)

page_b_content = ui.page_sidebar(
    ui.sidebar(
        ui.input_slider(
            "mass",
            "Mass",
            2000,
            6000,
            3400,
        ),
        ui.input_checkbox_group(
            "species", "Filter by species", species, selected=species
        ),
    ),
)

page_c_content = ui.page_fillable(
    ui.card(
        ui.card_header(ui.HTML("""<h1>Predict your own star! 🌌</h1>""")),
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
        class_ = "justify-content-center text-center"
    ),  
    ui.output_ui("text"),
)

app_ui = ui.page_navbar(
    ui.nav_panel("Constellations", page_a_content),
    ui.nav_panel("Stars", page_b_content),
    ui.nav_panel("Prediction", page_c_content),
    title="Celestial Insights ⭐",
    id="page",
    footer = ui.div(
        {
            "style": "width:100%; padding: 5px 0; text-align: center; border-top: 2px solid black;"
        },
        ui.tags.style(
            """
            h4 {
                color: black; /* White text on a light background might be hard to see, adjust if necessary */
            }
            .footer-text {
                font-size: 14px;
                color: black; /* Light gray for readability */
            }
            """
        ),
        ui.h4("✩₊˚.⋆☾⋆⁺₊", {"style": "margin-top: 0.3em; margin-bottom: 0.3em;"}), 
        ui.p("Made by Serena Gong (sxgong2) for CS498 Spring 2024, E2E Data Science", {"class": "footer-text"}) 
    )
)

def server(input: Inputs, output: Outputs, session: Session):
    @reactive.calc
    def filtered_df() -> pd.DataFrame:
        filt_df = df[df["Species"].isin(input.species())]
        filt_df = filt_df.loc[filt_df["Body Mass (g)"] > input.mass()]
        return filt_df

    @render.text
    def adelie_count():
        return count_species(filtered_df(), "Adelie")

    @render.text
    def chinstrap_count():
        return count_species(filtered_df(), "Chinstrap")

    @render.text
    def gentoo_count():
        return count_species(filtered_df(), "Gentoo")

    @render.plot
    def length_depth():
        return sns.scatterplot(
            data=filtered_df(),
            x="Bill Length (mm)",
            y="Bill Depth (mm)",
            hue="Species",
        )

    @render.data_frame
    def summary_statistics():
        display_df = filtered_df()[
            [
                "Species",
                "Island",
                "Bill Length (mm)",
                "Bill Depth (mm)",
                "Body Mass (g)",
            ]
        ]
        return render.DataGrid(display_df, filters=True)
    
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
                f"Your star's name is <b>{star_name}</b>, "
                f"with a right ascension of: <strong>{ra}</strong> and "
                f"declination: <strong>{dec}</strong>"                
                f"Predicted Constellation: {predictions[0]}, "
                "Probabilities of Predictions Adjusted for Model Accuracy:\n" +
                "\n".join(f"{constellation}: {prob*100:.2f}%" for constellation, prob in class_probabilities.items())
            )
            
            return (ui.card(
                ui.card_header("Results"),
                (result_text)
            ))


def count_species(df, species):
    return df[df["Species"] == species].shape[0]

app = App(app_ui, server)
if __name__ == "__main__":
    app.run()