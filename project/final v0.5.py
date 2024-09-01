from tmdbv3api import TMDb, Movie
import cpi
from datetime import datetime

tmdb = TMDb()
tmdb.api_key = ""


def main():

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
              movie_id = ask_overview(movie, movie_id)
              movie_id = ask_further_info(movie, movie_id)




def refine_search(list):


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

            detailed_info = movie.details(id)
            budget = detailed_info.get("budget", 0)
            revenue_b = detailed_info.get("revenue", 0)
            director, writers, top_actors = get_credits(movie, id)
            release_date = detailed_info.get("release_date", "N/A")
            year, month, day = release_date.split("-")

            revenue, year, budget = adjust_for_inflation(float(revenue_b), int(year), float(budget))

            estimated_profit = (revenue * 0.5) - budget



            print("\nSearch Results:")
            print(f"Title: {detailed_info.get('title', 'N/A')}")
            print(f"Runtime: {detailed_info.get('runtime', 'N/A')} minutes")
            print(f"Genre: {detailed_info.get('genre', 'N/A')}")
            print(f"Release Date: {detailed_info.get('release_date', 'N/A')}\n")
            print(f"Director: {director}")
            print(f"Writers: {format_list(writers)}")
            print(f"Top Billed: {format_list(top_actors)}\n")
            print(f"Budget: ${detailed_info.get('budget', 0): ,}")
            print(f"Revenue: ${revenue:,.2f}")
            print(f"Estimated Profit: ${estimated_profit:,}\n")
            print("\x1B[3mEstimated profit is a rough calculation that doesn't account for country-specific revenues or additional costs beyond the initial budget.\x1B[0m\n")
            return id



def ask_overview(movie, n):

    try:
        ask_input =input("Would you like a synopsis? Y/N  ").upper()
        if ask_input == "Y":
            detailed_info = movie.details(n)
            print(f"Synopsis: {detailed_info.get('overview', 'N/A')}\n")
        elif ask_input == "N":
            return n
        else:
            print("Invalid choice, Y/N ONLY")
    except ValueError:
        print("Invalid: Must Be Y/N")
    return n




def ask_further_info(movie, n):

     questions = [
          "Full Cast and Crew",
          "Trailer",
          "Production infomation",
          "Extra facts",
          "Website",
          "Tagline"
          ]

     actions = {
          1: get_full_cast_and_crew,
          2: get_trailer,
          3: get_production_information,
          4: get_extra_facts,
          5: get_website,
          6: get_tagline
          }
     while True:
        for i, question in enumerate(questions, start=1):
            print(f"{i}. {question}")
        print("\nEnter 'exit' to return to the main menu\n")

        choice_f = input("Pick an option: ")

        if choice_f.lower() == "exit":
            break

        try:

            choice_f = int(choice_f)

            if 1 <= choice_f <= len(questions):
                action = actions[choice_f]
                action(movie, n)
            else:
                print("Invalid choice")
        except ValueError:
                print("Invalid input. Pick a number")




def get_full_cast_and_crew(movie, n):
     credits = movie.credits(n)
     crew = list(credits.get("crew", []))
     cast = list(credits.get("cast", []))
     full_credits = cast + crew
     for member in full_credits:
          print(f"{member.get('name')} - {member.get('job', member.get('character', ''))}\n")


def get_trailer(movie, n):


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
     details = movie.details(n)

     companies =  details.get("production_companies", [])
     countries =  details.get("production_countries", [])
     original_lang =  details.get("original_language", [])
     company_names = [company["name"] for company in companies]
     country_names = [country["name"] for country in countries]

     print(f"Production Companies: {','.join(company_names)}\n")
     print(f"Production Countries: {','.join(country_names)}\n")
     print(f"Production Language: {original_lang}\n")


def get_extra_facts(movie, n):
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
     details = movie.details(n)
     website_info = details.get("website")
     print(f"Website: {website_info}\n")


def get_tagline(movie, n):
     details = movie.details(n)
     tagline = details.get("tagline")
     print(f"Movie's tagline: {tagline}\n")



def get_credits(movie, id):
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
     return ", ".join(list) if list else "N/A"

def adjust_for_inflation(rev, year, budget):
    try:
        if year < 1990:
            current_year = int(datetime.now().year)
            current_year = current_year - 1 #CPI data is only for the previous year.
            answer_input = input("Would you like Box Office information adjusted for inflation? Y/N ").upper()
            if answer_input == "Y":
                rev = round(cpi.inflate(rev, year, to=current_year), 2)
                budget = round(cpi.inflate(budget, year, to=current_year), 2)
    except Exception as e:
        print(f"Inflation adjustment error: {e}")
    return rev, year, budget






if __name__ == "__main__":
    main()
