import cpi
def main():
    rev = 1000
    budget = 10000

    year = 1950
    current_year = 2023



    rev = round(cpi.inflate(rev, year, to=current_year), 2)
    budget = round(cpi.inflate(budget, year, to=current_year), 2)

    print(f"Latest available year in CPI data: {cpi.LATEST_YEAR}")


    print(f"{rev} is the revenue, and {budget} is the budget, adjusted for inflation")
main()
