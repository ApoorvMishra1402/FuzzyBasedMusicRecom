import pandas as pd


music_data = pd.read_csv("cleaned_data.csv")

# Read user preferences
user_preferences = {
    "Electronic": 0.5,
    "Rap": 0.9,
    "Anime": 0.2,
    "Hip-Hop": 0.6,
    "Jazz": 0.3,
    "Blues": 0.2,
    "Country": 0.4,
    "Alternative": 0.1,
    "Classical": 0.3,
    "Rock": 0.5,
    "Popularity": 0.5,  # Add popularity preference
    "Acousticness": 0.3,  # Add acousticness preference
    "Duration_ms": 0.4,  # Add duration preference
    "Energy": 0.1,  # Add energy preference
    "Loudness": 0.2,  # Add loudness preference
    # Add parameters for other features
}

# Define trapezoidal membership
def trapezoidal_membership(x, params):
    lower_left = params["lower_left"]
    lower_peak = params["lower_peak"]
    upper_peak = params["upper_peak"]
    upper_right = params["upper_right"]

    if x <= lower_left or x >= upper_right:
        return 0
    elif lower_left <= x <= lower_peak:
        return (x - lower_left) / (lower_peak - lower_left)
    elif lower_peak <= x <= upper_peak:
        return 1
    else:
        return (upper_right - x) / (upper_right - upper_peak)

# Define fuzzy inference for song recommendation
def fuzzy_inference(preferences, music_data):
    recommendations = {}

    for song_index, song_row in music_data.iterrows():
        track_name = song_row["track_name"]
        recommendation_strength = 0

        for preference, preference_value in preferences.items():
            # Ensure the preference is in the data columns
            if preference in music_data.columns:
                membership_value_for_feature = song_row[preference]
                membership_params = {
                            "Electronic": {"lower_left": 0.2, "lower_peak": 0.4, "upper_peak": 0.6, "upper_right": 0.8},
        "Rap": {"lower_left": 0.1, "lower_peak": 0.3, "upper_peak": 0.7, "upper_right": 0.9},
        "Anime": {"lower_left": 0.0, "lower_peak": 0.2, "upper_peak": 0.5, "upper_right": 0.7},
        "Hip-Hop": {"lower_left": 0.1, "lower_peak": 0.4, "upper_peak": 0.6, "upper_right": 0.8},
        "Jazz": {"lower_left": 0.2, "lower_peak": 0.5, "upper_peak": 0.7, "upper_right": 0.9},
        "Blues": {"lower_left": 0.1, "lower_peak": 0.4, "upper_peak": 0.6, "upper_right": 0.8},
        "Country": {"lower_left": 0.0, "lower_peak": 0.2, "upper_peak": 0.5, "upper_right": 0.7},
        "Alternative": {"lower_left": 0.1, "lower_peak": 0.4, "upper_peak": 0.6, "upper_right": 0.8},
        "Classical": {"lower_left": 0.2, "lower_peak": 0.5, "upper_peak": 0.7, "upper_right": 0.9},
        "Rock": {"lower_left": 0.1, "lower_peak": 0.4, "upper_peak": 0.6, "upper_right": 0.8},
        "Pop": {"lower_left": 0.0, "lower_peak": 0.3, "upper_peak": 0.6, "upper_right": 0.9},
        "Reggae": {"lower_left": 0.0, "lower_peak": 0.2, "upper_peak": 0.5, "upper_right": 0.8},
        "Metal": {"lower_left": 0.1, "lower_peak": 0.4, "upper_peak": 0.7, "upper_right": 0.9},
        "Funk": {"lower_left": 0.1, "lower_peak": 0.3, "upper_peak": 0.6, "upper_right": 0.8},
        "R&B": {"lower_left": 0.1, "lower_peak": 0.3, "upper_peak": 0.7, "upper_right": 0.9},
                }  # Define appropriate membership parameters

                # Calculate membership using trapezoidal_membership function
                membership_function = trapezoidal_membership(
                    membership_value_for_feature, membership_params)
                recommendation_strength += preference_value * membership_function

        recommendations[track_name] = recommendation_strength

    # Choose the song with the highest recommendation strength
    recommended_song = max(recommendations, key=recommendations.get)
    return recommended_song

# Make music song recommendations
recommended_song = fuzzy_inference(user_preferences, music_data)
print("Recommended Song:", recommended_song)
