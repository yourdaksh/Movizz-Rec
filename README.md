# Movie Recommendation System using Streamlit

This is a simple movie recommendation system built using Python and Streamlit. The system recommends movies similar to the one you select.

## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

- Python 3.x
- Streamlit
- Pandas
- Requests

### Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/Adarshh9/MRS.git
```

2. Install the required Python packages using pip:

```bash
pip install streamlit pandas requests
```

### Usage

1. Run the Streamlit app:

```bash
streamlit run app.py
```

2. Access the app through your web browser.

3. Select a movie from the dropdown menu and click the "Recommend" button.

4. The app will display a list of recommended movies along with their posters.

## Features

- Select a movie from the dropdown menu.
- Get a list of recommended movies based on similarity.
- View movie posters for the recommended movies.

## Implementation Details

The project consists of two main parts: data preprocessing and the Streamlit web app.

### Data Preprocessing

1. The movie data is loaded from CSV files (`tmdb_5000_movies.csv` and `tmdb_5000_credits.csv`).

2. Data cleaning is performed, including handling missing values and duplicate records.

3. Movie attributes like genres, keywords, cast, and crew are extracted and preprocessed.

4. Text data is tokenized and stemmed for vectorization.

5. Count vectorization is applied to convert text data into numerical features.

6. Cosine similarity is calculated between movies based on their feature vectors.

7. Similarity scores are stored in a compressed pickle file.

### Streamlit Web App

1. The Streamlit app is created to provide a user interface.

2. Users can select a movie from the dropdown menu.

3. When the "Recommend" button is clicked, the app fetches and displays recommended movies based on the selected movie.

4. Movie posters are fetched from an external API and displayed alongside the movie titles.

## Files

- `app.py`: The Streamlit web app for movie recommendations.
- `tmdb_5000_movies.csv`: Movie data in CSV format.
- `tmdb_5000_credits.csv`: Credits data in CSV format.
- `movie_dict.pickle`: Preprocessed movie data in a pickled dictionary format.
- `similarity3.xz`: Compressed pickle file containing cosine similarity scores.

## Acknowledgments

- Movie data is sourced from [The Movie Database (TMDb)](https://www.themoviedb.org/).
- The project is inspired by various online tutorials and resources.

## Deployment

The movie recommendation system is deployed on [Streamlit Cloud](https://movizz.streamlit.app/). You can access and use the system by visiting the following link:

[Movie Recommendation System on Streamlit Cloud](https://movizz.streamlit.app/)

Feel free to try it out and discover movie recommendations based on your preferences!

## Getting Involved

Contributions to this project are always welcome. If you'd like to contribute, please follow the instructions in the [Contributing Guidelines](CONTRIBUTING.md).

If you encounter any issues or have suggestions for improvement, please don't hesitate to [open an issue](https://github.com/your/repository/issues). Your feedback and contributions help make this project better for everyone.

## Acknowledgments

- Special thanks to [TMDb](https://www.themoviedb.org/) for providing the movie data.
- This project was created for educational purposes and is not affiliated with TMDb.

--------------------------------------------------------------------------------------------------
