import pandas as pd


music_data = pd.read_csv("cleaned_music_data.csv")

# Read user preferences
user_preferences = {
    "Electronic": 0.7,
    "Rap": 0.3,
    "Anime": 0.5,
    "Hip-Hop": 0.8,
    "Jazz": 0.4,
    "Blues": 0.2,
    "Country": 0.6,
    "Alternative": 0.9,
    "Classical": 0.3,
    "Rock": 0.7,
   
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

#fuzzy inference for song recommendation

def fuzzy_inference(preferences, music_data):
    recommendations = {}

   
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
        
    }

    for genre in preferences:
        # Ensure the genre is in the membership parameters dictionary
        if genre in membership_params:
            membership_value = preferences[genre]
            params = membership_params[genre]

            # Calculate membership using trapezoidal_membership function
            membership_function = trapezoidal_membership(
                membership_value, params)

            if membership_function > 0:
                recommendations[genre] = membership_function * 0.8

    # Choose the genre with the highest recommendation strength
    recommended_genre = max(recommendations, key=recommendations.get)
    return recommended_genre

# Make music genre recommendations
recommended_genre = fuzzy_inference(user_preferences, music_data)
print("Recommended Genre:", recommended_genre)
