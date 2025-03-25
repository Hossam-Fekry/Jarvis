from googlesearch import search
from webbrowser import open

def search_google(topic):
    # Prompt user for input
    query = topic

    try:
        # Fetch search results from Google
        speak("\nSearch results for", query, ":\n")
        results = list(search(query, num_results=2))  # Fetching top 2 results

        if results:
            # Check if the first result is a Google link
            if "google" in results[0]:
                speak("First result is a Google link. Opening the second result...")
                open(results[1])  # Open the second result
            else:
                speak("Opening the first result...")
                open(results[0])  # Open the first result
        else:
            speak("No results found.")

    except Exception as e:
        speak("An error occurred:", e)

if __name__ == "__main__":
    search_google("ELon Musk")