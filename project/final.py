"""
This is a movie information resource that asks users for a movie title then refines that input to accurate find information about that movie.
The information displayed is choosen by the user through rudimentary menus.
"""

from tmdbv3api import TMDb, Movie
from datetime import datetime
from dotenv import load_dotenv
import sys
import os

cpi_library = None
load_dotenv()
tmdb = TMDb()
tmdb.api_key = os.getenv("MY_KEY")

def main():
    """
    Main function that runs the movie search engine.

    This function proceeds through the following steps:
    1. Asks for user input in the form of a movie title, or quit
    2. Requests movie details that match the user input through API to The Movie DB(TMDB)
    3. The results are sorted by the popularity metric provided by TMDB then printed for user selection
    4. Basic information from the selected film is print, full Title, runtime, Director, writer, and top billed actors.
    5. User is then prompted to choose one of the following options:
        -Full Cast and Crew
        -Trailer
        -Production infomation
        -Synopsis
        -Website
        -Tagline
        -Extra Facts

    The main loop allows the user to choose further informtion, return to search, or exit.

    See Also:
        This program relies heavily on library tmdbv3api created by Anthony Bloomer
        Further information on those functions can be found at:
        https://github.com/AnthonyBloomer/tmdbv3api
    """


    movie = Movie()

    while True:
         input_title = input("Please enter a movie title, or quit to quit: ").strip().title()
         if input_title.lower() == "quit":
              print("Exitting...")
              break
         results = movie.search(input_title)
         if not results:
              print("No results found. Please check input.")
              continue

         sorted_results = sorted(results, key=lambda x: x["popularity"], reverse=True)
         top_5_res = sorted_results[:5]
         movie_id = refine_search(top_5_res)
         if movie_id:
              movie_id = details(movie, movie_id)
              movie_id = ask_further_info(movie, movie_id)



def refine_search(list):
    """
    Takes list of movies from user input query then refines it to aquire movie id

    Args:
        list (list): Top 5 movies that conform to user input sorted by popularity

    Returns:
        movie id or error if input error
    """

    print("Top 5 Results:")
    for idx, results in enumerate(list, start=1):
        title = results.get("title", "N/A")
        release_date = results.get("release_date", "N/A")
        print(f"{title} ({release_date}) - {idx}\n")

    try:
        input_choice = int(input("Which movie did you mean? Please specify the number: "))
        if 1 <= input_choice <= 5:
            selected_movie = list[input_choice - 1]
            movie_id = selected_movie.get("id")
            return movie_id

        else:
                print("Invalid: Pick 1-5 ONLY")

    except ValueError:
            print("Invalid: Must be number between 1 and 5")
    return None



def details(movie, id):
            """
            Takes movie then queries TMDB for basic information on movie that's formatted then printed

            Args:
                tmdbv3api's movie instance
                id (int): movie id from TMDB

            Returns:
                Prints various basic movie facts that would be found on a poster
                id of the movie
            """

            detailed_info = movie.details(id)
            director, writers, top_actors = get_credits(movie, id)


            print("\nSearch Results:")
            print(f"Title: {detailed_info.get('title', 'N/A')}")
            print(f"Runtime: {detailed_info.get('runtime', 'N/A')} minutes")
            print(f"Release Date: {detailed_info.get('release_date', 'N/A')}\n")
            print(f"Director: {director}")
            print(f"Writers: {format_list(writers)}")
            print(f"Top Billed: {format_list(top_actors)}\n")
            return id



def ask_further_info(movie, n):
     """
     Presents user with list of options each item is a function to query DB for that information exit and return inputs allow user to navigate out or back

     Args:
        movie : tmdbv3api's movie instance
        n (int): movie id
    Returns:
        List of options for user to pick
        Allows user to exit
     """

     questions = [
          "Full Cast and Crew",
          "Trailer",
          "Production infomation",
          "Synopsis",
          "Website",
          "Tagline",
          "Extra Facts"
          ]

     actions = {
          1: get_full_cast_and_crew,
          2: get_trailer,
          3: get_production_information,
          4: get_synopsis,
          5: get_website,
          6: get_tagline,
          7: get_extra_facts
          }
     while True:
        for i, question in enumerate(questions, start=1):
            print(f"{i}. {question}")
        print("\nEnter 'return' to search for another movie! Or, exit to exit.\n")

        choice_f = input("Pick an option: ")

        if choice_f.lower() == "return":
            break
        if choice_f.lower() == "exit":
             print("Exitting...")
             sys.exit()

        try:

            choice_f = int(choice_f)

            if 1 <= choice_f <= len(questions):
                action = actions[choice_f]
                action(movie, n)
            else:
                print("Invalid choice")
        except ValueError:
                print("Invalid input. Pick a number")


def get_synopsis(movie, n):
     """
     Uses movie id to retrieve synopsis

     Args:
        movie : tmdbv3api's movie instance
        n (int): movie id
     Returns:
        Prints movie synopsis
     """

     detailed_info = movie.details(n)
     print(f"Synopsis: {detailed_info.get('overview', 'N/A')}\n")



def get_full_cast_and_crew(movie, n):
     """
     Retrieves credits

     Args:
        movie : tmdbv3api's movie instance
        n (int): movie id

     Returns:
        Prints formated credits line by line
     """

     credits = movie.credits(n)
     crew = list(credits.get("crew", []))
     cast = list(credits.get("cast", []))
     full_credits = cast + crew
     for member in full_credits:
          print(f"{member.get('name')} - {member.get('job', member.get('character', ''))}\n")



def get_trailer(movie, n):
    """
    Retrieves trailer link

    Args:
        movie : tmdbv3api's movie instance
        n (int): movie id

    Returns:
        Prints usable link to video on Youtube.com
    """

    details = movie.videos(n)
    video = details.get("results", [])

    if video:
        print("\nTrailers:\n")
        for vid in video:
            video_title = vid.get("name", "No Title")
            video_key = vid.get("key")
            video_url = f"http://www.youtube.com/watch?v={video_key}"
            print(f"{video_title}: {video_url}\n")



def get_production_information(movie, n):
     """
     Gets production information, such as company, budget, revenue, calculates profit from given information.


     Args:
        movie : tmdbv3api's movie instance
        n (int): movie id

     Returns:
        Prints production information
        Also checks year movie is made then pings user for inflation calculation if older than 1990

     """
     details = movie.details(n)
     companies =  details.get("production_companies", [])
     countries =  details.get("production_countries", [])
     original_lang =  details.get("original_language", [])
     budget = details.get("budget", 0)
     revenue_b = details.get("revenue", 0)
     company_names = [company["name"] for company in companies]
     country_names = [country["name"] for country in countries]
     release_date = details.get("release_date", "N/A")
     year, month, day = release_date.split("-")


     revenue, year, budget = adjust_for_inflation(float(revenue_b), int(year), float(budget))
     estimated_profit = (revenue * 0.5) - budget


     print(f"Production Companies: {','.join(company_names)}\n")
     print(f"Production Countries: {','.join(country_names)}\n")
     print(f"Production Language: {original_lang}\n")
     print(f"Budget: ${budget:,.2f}")
     print(f"Revenue: ${revenue:,.2f}")
     print(f"Estimated Profit: ${estimated_profit:,.2f}\n")
     print("\x1B[3mEstimated profit is a rough calculation that doesn't account for country-specific revenues or additional costs beyond the initial budget.\x1B[0m\n")



def get_extra_facts(movie, n):
    """
    Retrieves extra information for movie that didn't fit other categories


    Args:
        movie : tmdbv3api's movie instance
        n (int): movie id

    Returns:
        Prints original title, Alternative title, Genre, and Spoken language

    """

    details = movie.details(n)
    original_title = details.get("original_title")
    alt_title =  details.get("alternative_titles", [])
    genres = details.get("genres", [])

    spoke_lang = details.get("spoken_languages", [])
    genre_names = [genre["name"] for genre in genres]
    spoken_lang_name = [sp_lang["name"] for sp_lang in spoke_lang]

    print(f"Original Title: {original_title}")
    print(f"Alternative Title: {alt_title}\n")
    print(f"Genre: {','.join(genre_names)}\n")

    print(f"Spoken Language: {spoken_lang_name}\n")



def get_website(movie, n):
    """
    Retrieves website link for movie

    Args:
        movie : tmdbv3api's movie instance
        n (int): movie id

    Returns:
        Prints link to the movie's website
    """

    details = movie.details(n)
    website_info = details.get("website")
    print(f"Website: {website_info}\n")



def get_tagline(movie, n):
    """
    Retrieves tagline

    Args:
        movie : tmdbv3api's movie instance
        n (int): movie id

    Returns:
        Prints tagline for movie
    """

    details = movie.details(n)
    tagline = details.get("tagline")
    print(f"Movie's tagline: {tagline}\n")



def get_credits(movie, id):
    """
    Retrieves credits then splits that into Director, up to 3 writers, and first 5 billed actors

    Args:
        movie : tmdbv3api's movie instance
        n (int): movie id

    Returns:
        Prints top 5 actors as Top Billed, Director, and up to 3 Writers
    """

    credits = movie.credits(id)
    director = None
    writers = []
    top_actors = []
    crew = credits.get("crew", [])
    cast = credits.get("cast", [])

    for crew_member in crew:
         if crew_member.get("job") == "Director" and director is None:
              director = crew_member.get("name")
         elif crew_member.get("job") in ["Writer", "Screenplay", "Story"] and len(writers) < 3:
              writers.append(crew_member.get("name"))


    for i in range(min(5, len(cast))):
        actor = cast[i]
        top_actors.append(actor.get("name"))

    if director is None:
        director = "\x1BN/A\x1B[0m"
    if len(writers) == 0:
        writers = ["\x1BN/A\x1B[0m"]
    if len(top_actors) == 0:
        top_actors = ["\x1BN/A\x1B[0m"]

    return director, writers, top_actors



def format_list(list):
    """
    Formats lists so they print correctly

    Args:
        list (list): list of names

    Returns:
        Formated list with proper spacing or fills list with "N/A" if empty
    """


    return ", ".join(list) if list else "N/A"



def adjust_for_inflation(rev, year, budget):
    """
    Checks production year and if before 1990 asks user if they want to adjust monetary figures for inflation

    Args:
        rev (int): revenue of movie
        year (int): year of movie as int
        budget (int): budget of movie

    Returns:
        Depending on user input:
        if Y, outputs budget, rev, and profit adjusted for inflation by CPI library
        if N, or film after 1990, returns budget, rev, and profit as found in TMDB

    """


    try:
        if year < 1990:
            current_year = int(datetime.now().year)
            current_year = current_year - 1 #CPI data is only for the previous year.
            answer_input = input("Would you like Box Office information adjusted for inflation? Y/N ").upper()
            if answer_input == "Y":
                print("Please wait, calculating...")
                initialize_cpi_library()
                rev = round(cpi_library.inflate(rev, year, to=current_year), 2)
                budget = round(cpi_library.inflate(budget, year, to=current_year), 2)
    except Exception as e:
        print(f"Inflation adjustment error: {e}")
    return rev, year, budget

def initialize_cpi_library():
     """
     Initializes the cpi library only when inflation adjustment is request to prevent lag time at program start up.

     Args:
        None
     Returns:
        cpi object
     """
     global cpi_library
     if cpi_library is None:
          import cpi
          cpi_library = cpi



if __name__ == "__main__":
    main()
