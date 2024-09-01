<!-- markdownlint-disable -->
# Movie Information Hotline
    #### Video Demo:  <URL HERE>


# Description:

<a href="../../project/final.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `final.py`
This is a movie information resource that uses terminal interface to ask for a movie title then refines that input to accurate find information about that movie. The information displayed is choosen by the user through rudimentary menus.

**Global Variables**
---------------

- **cpi_library** Allows the CPI library to be intialized only when required for use as it would generate considerable lag that I couldn't find a way to avoid. 
- **API KEY** The api key is provided to the function by way of .env file, an example is included, .env.example use this to make your own key.
  
---

<a href="../../project/final.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `main`

```python
main()
```

Main function that runs the movie search engine.

This function proceeds through the following steps: 1. Asks for user input in the form of a movie title, or quit 2. Requests movie details that match the user input through API to The Movie DB(TMDB) 3. The results are sorted by the popularity metric provided by TMDB then printed for user selection 4. Basic information from the selected film is print, full Title, runtime, Director, writer, and top billed actors. 5. User is then prompted to choose one of the following options:
    -Full Cast and Crew
    -Trailer
    -Production infomation
    -Synopsis
    -Website
    -Tagline
    -Extra Facts

The main loop allows the user to choose further informtion, return to search, or exit.

See Also:  This program relies heavily on library tmdbv3api created by Anthony Bloomer  Further information on those functions can be found at:  https://github.com/AnthonyBloomer/tmdbv3api


---

<a href="../../project/final.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `refine_search`

```python
refine_search(list)
```

Takes list of movies from user input query then refines it to aquire movie id



**Args:**

 - <b>`list`</b> (list):  Top 5 movies that conform to user input sorted by popularity



**Returns:**
 movie id or error if input error


---

<a href="../../project/final.py#L96"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `details`

```python
details(movie, id)
```

Takes movie then queries TMDB for basic information on movie that's formatted then printed



**Args:**
  tmdbv3api's movie instance
 - <b>`id`</b> (int):  movie id from TMDB



**Returns:**
 Prints various basic movie facts that would be found on a poster id of the movie


---

<a href="../../project/final.py#L124"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `ask_further_info`

```python
ask_further_info(movie, n)
```

Presents user with list of options each item is a function to query DB for that information exit and return inputs allow user to navigate out or back



**Args:**

  - <b>`movie `</b>:  tmdbv3api's movie instance
  - <b>`n`</b> (int):  movie id

**Returns:**
 List of options for user to pick Allows user to exit




---

<a href="../../project/final.py#L181"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_synopsis`

```python
get_synopsis(movie, n)
```

Uses movie id to retrieve synopsis



**Args:**

 - <b>`movie `</b>:  tmdbv3api's movie instance
 - <b>`n`</b> (int):  movie id

**Returns:**
 Prints movie synopsis


---

<a href="../../project/final.py#L197"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_full_cast_and_crew`

```python
get_full_cast_and_crew(movie, n)
```

Retrieves credits



**Args:**

 - <b>`movie `</b>:  tmdbv3api's movie instance
 - <b>`n`</b> (int):  movie id



**Returns:**
 Prints formated credits line by line


---

<a href="../../project/final.py#L218"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_trailer`

```python
get_trailer(movie, n)
```

Retrieves trailer link



**Args:**

 - <b>`movie `</b>:  tmdbv3api's movie instance
 - <b>`n`</b> (int):  movie id



**Returns:**
 Prints usable link to video on Youtube.com


---

<a href="../../project/final.py#L243"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_production_information`

```python
get_production_information(movie, n)
```

Gets production information, such as company, budget, revenue, calculates profit from given information.





**Args:**

 - <b>`movie `</b>:  tmdbv3api's movie instance
 - <b>`n`</b> (int):  movie id



**Returns:**
 Prints production information Also checks year movie is made then pings user for inflation calculation if older than 1990


---

<a href="../../project/final.py#L283"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_extra_facts`

```python
get_extra_facts(movie, n)
```

Retrieves extra information for movie that didn't fit other categories





**Args:**

 - <b>`movie `</b>:  tmdbv3api's movie instance
 - <b>`n`</b> (int):  movie id



**Returns:**
 Prints original title, Alternative title, Genre, and Spoken language


---

<a href="../../project/final.py#L314"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_website`

```python
get_website(movie, n)
```

Retrieves website link for movie



**Args:**

 - <b>`movie `</b>:  tmdbv3api's movie instance
 - <b>`n`</b> (int):  movie id



**Returns:**
 Prints link to the movie's website


---

<a href="../../project/final.py#L332"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_tagline`

```python
get_tagline(movie, n)
```

Retrieves tagline



**Args:**

 - <b>`movie `</b>:  tmdbv3api's movie instance
 - <b>`n`</b> (int):  movie id



**Returns:**
 Prints tagline for movie


---

<a href="../../project/final.py#L350"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_credits`

```python
get_credits(movie, id)
```

Retrieves credits then splits that into Director, up to 3 writers, and first 5 billed actors



**Args:**

 - <b>`movie `</b>:  tmdbv3api's movie instance
 - <b>`n`</b> (int):  movie id



**Returns:**
 Prints top 5 actors as Top Billed, Director, and up to 3 Writers


---

<a href="../../project/final.py#L391"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `format_list`

```python
format_list(list)
```

Formats lists so they print correctly



**Args:**

 - <b>`list`</b> (list):  list of names



**Returns:**
 Formated list with proper spacing or fills list with "N/A" if empty


---

<a href="../../project/final.py#L407"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `adjust_for_inflation`

```python
adjust_for_inflation(rev, year, budget)
```

Checks production year and if before 1990 asks user if they want to adjust monetary figures for inflation



**Args:**

 - <b>`rev`</b> (int):  revenue of movie
 - <b>`year`</b> (int):  year of movie as int
 - <b>`budget`</b> (int):  budget of movie



**Returns:**
 Depending on user input: if Y, outputs budget, rev, and profit adjusted for inflation by CPI library if N, or film after 1990, returns budget, rev, and profit as found in TMDB


---

<a href="../../project/final.py#L438"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `initialize_cpi_library`

```python
initialize_cpi_library()
```

Initializes the cpi library only when inflation adjustment is request to prevent lag time at program start up.



**Args:**
  None

**Returns:**
  cpi object




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
