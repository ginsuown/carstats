from requests import get
from bs4 import BeautifulSoup
import time
import json

base_url = "https://www.carspecs.us"
cars_container = []

# 0/1 to show cars as they are scraped
show_individual_car = 0

# limits to speed up debugging
makes_limit = 0
models_limit = 0
years_limit = 0
trims_limit = 0


def make_soup(url):
    return BeautifulSoup(get(url).text, "html.parser")


def get_makes():
    # progress display
    total = 0
    current_make = ""
    print("scraping makes...")

    # base url
    url = base_url
    soup = make_soup(url)

    # store scraped makes
    makes = []

    # make_chunk because list of makes is split into many sections
    for make_chunk in soup.find_all("ul", class_="pure-u-1 pure-u-lg-1-4 pure-u-md-1-2"):
        # limit makes to speed up debugging
        if makes_limit != 0 and total > makes_limit:
            print("")
            return makes

        # list of li's in the chunk
        li_tags = make_chunk.find_all("li")

        # for each li, scrape url and append
        for li in li_tags:
            current_make = li.a.text
            total += 1
            link = li.a["href"]
            makes.append(link)

            # update progress log
            print('  {}; {}            '.format(total, current_make), end="\r")
            time.sleep(0.01)
    print("")
    return makes


def get_models(makes):
    # progress display
    total = 0
    current_make = ""
    current_model = ""
    print("scraping models...")

    # store scraped models
    models = []

    # use array of makes
    for make in makes:
        # limit to speed up debugging
        if models_limit != 0 and total > models_limit:
            print("")
            return models

        # construct full url
        url = base_url + make
        soup = make_soup(url)
        parent_tag = soup.find("h2", text="SELECT A MODEL").parent.ul
        ul = parent_tag.find_all("li")
        current_make = soup.find("h1").b.text
        # for each li, scrape url and save
        for li in ul:
            current_model = li.a.text
            total += 1
            link = li.a["href"]
            models.append(link)

            # update progress log
            print('  {}; {} {}                                   '.format(total, current_make, current_model), end="\r")
            time.sleep(0.01)
    print("")
    return models


def get_years(models):
    # progress display
    total = 0
    current_make_model = ""
    print("scraping years...")

    # store scraped models
    years = []

    # use array of models
    for model in models:
        # limit to speed up debugging
        if years_limit != 0 and total > years_limit:
            print("")
            return years

        # construct full url
        url = base_url + model
        soup = make_soup(url)
        parent_tag = soup.find("h2", text="SELECT A YEAR").parent.ul
        ul = parent_tag.find_all("li")
        # for each li, scrape url and save
        for li in ul:
            current_make_model = soup.h1.text
            current_year = li.a.text
            total += 1
            link = li.a["href"]
            years.append(link)

            # update progress log
            print('  {}; {} {}                                       '.format(total, current_make_model, current_year), end="\r")
            time.sleep(0.01)
    print("")
    return years


def get_trims(years):
    # progress display
    total = 0
    current_car = ""
    current_trim = ""
    print("scraping trims...")

    # store scraped trims
    trims = []

    # use array of makes
    for year in years:
        # limit to speed up debugging
        if trims_limit != 0 and total > trims_limit:
            print("")
            return trims
        # construct full url
        url = base_url + year
        soup = make_soup(url)
        selector = soup.find("select", id="selected-trim")
        ul = selector.find_all("option")

        # for each li, scrape url and save
        for li in ul:
            current_car = soup.find("h1").b.text
            current_trim = li.text
            total += 1
            trims.append(li["value"])
            # update progress log
            print('  {}; {} {}                             '.format(total, current_car, current_trim), end="\r")
            time.sleep(0.01)
    print("")
    return trims


# scrape cars and store in db
def scrape_cars(all_cars):
    # progress display
    total = 0
    print("{} car(s) found, now scraping specs...".format(len(all_cars)))

    for car in all_cars:
        result = scrape_car(car)
        current_car = result["year"] + " " + \
            result["make"] + " " + result["name"]
        total += 1

        # update progress log
        print("  {}% done...".format(format(total/len(all_cars)*100, '.2f')), end="\r")
        # put into cars_container
        cars_container.append(result)

    print("Successfully scraped {} car(s)!".format(total))


def scrape_car(trim):

    # construct url
    url = base_url + trim
    soup = make_soup(url)

    car = {}
    full_name = soup.find(
        'div', class_="pure-u-1 pure-u-md-17-24").find_all("a")

    car["year"] = soup.find('h1').text[0:4] if soup.find('h1') else None

    car["name"] = full_name[2].text

    car["make"] = full_name[1].text

    car["zero_to_sixty"] = soup.find('h4', text="0-60 mph").parent.text.splitlines()[
        2] if soup.find('h4', text="0-60 mph") else None

    car["hp"] = soup.find('h4', text="Horsepower").parent.text.splitlines()[
        2] if soup.find('h4', text="Horsepower") else None

    car["hp_rpm"] = soup.find('h4', text="Horsepower RPM").parent.text.splitlines()[
        2] if soup.find('h4', text="Horsepower RPM") else None

    car["torque"] = soup.find('h4', text="Torque").parent.text.splitlines()[
        2] if soup.find('h4', text="Torque") else None

    car["torque_rpm"] = soup.find('h4', text="Torque RPM").parent.text.splitlines()[
        2] if soup.find('h4', text="Torque RPM") else None

    car["cylinders"] = soup.find('h4', text="Cylinders").parent.text.splitlines()[
        2] if soup.find('h4', text="Cylinders") else None

    car["displacement"] = soup.find('h4', text="Base engine size").parent.text.splitlines()[
        2] if soup.find('h4', text="Base engine size") else None

    car["curb_weight"] = soup.find('h4', text="Curb weight").parent.text.splitlines()[
        2] if soup.find('h4', text="Curb weight") else None

    car["front_diameter"] = soup.find('h4', text="Front Wheel Diameter").parent.text.splitlines()[
        2] if soup.find('h4', text="Front Wheel Diameter") else None

    car["front_width"] = soup.find('h4', text="Front Wheel Width").parent.text.splitlines()[
        2] if soup.find('h4', text="Front Wheel Width") else None

    car["front_tire"] = soup.find('h4', text="Front Tire Size").parent.text.splitlines()[
        2] if soup.find('h4', text="Front Tire Size") else None

    car["rear_diameter"] = soup.find('h4', text="Rear Wheel Diameter").parent.text.splitlines()[
        2] if soup.find('h4', text="Rear Wheel Diameter") else None

    car["rear_width"] = soup.find('h4', text="Rear Wheel Width").parent.text.splitlines()[
        2] if soup.find('h4',  text="Rear Wheel Width") else None

    car["rear_tire"] = soup.find('h4', text="Rear Tire Size").parent.text.splitlines()[
        2] if soup.find('h4',  text="Rear Tire Size") else None

    car["length"] = soup.find('h4', text="Length").parent.text.splitlines()[
        2] if soup.find('h4', text="Length") else None

    car["width"] = soup.find('h4', text="Width").parent.text.splitlines()[
        2] if soup.find('h4', text="Width") else None

    car["height"] = soup.find('h4', text="Height").parent.text.splitlines()[
        2] if soup.find('h4', text="Height") else None

    # if show_individual_car:
    #     # print car stats
    #     if name:
    #         print("\nName: " + name)
    #     if zero_to_sixty:
    #         print("0-60 mph: " + zero_to_sixty)
    #     if hp:
    #         print("Horsepower: " + hp)
    #     if hp_rpm:
    #         print("Horsepower RPM: " + hp_rpm)
    #     if torque:
    #         print("Torque: " + torque)
    #     if torque_rpm:
    #         print("Torque RPM: " + torque_rpm)
    #     if cylinders:
    #         print("Cylinders: " + cylinders)
    #     if displacement:
    #         print("Displacement: " + displacement)
    #     if curb_weight:
    #         print("Curb Weight: " + curb_weight)
    #     if front_diameter:
    #         print("Front Wheel Diameter: " + front_diameter)
    #     if front_width:
    #         print("Front Wheel Width: " + front_width)
    #     if front_tire:
    #         print("Front Tire Size: " + front_tire)
    #     if rear_diameter:
    #         print("Rear Wheel Diameter: " + rear_diameter)
    #     if rear_width:
    #         print("Rear Wheel Width: " + rear_width)
    #     if rear_tire:
    #         print("Rear Tire Size: " + rear_tire)
    #     if length:
    #         print("Length: " + length)
    #     if width:
    #         print("Width: " + width)
    #     if height:
    #         print("Height: " + height)

    return car


def dump_data():
    with open('data.json', 'w') as outfile:
        json.dump(cars_container, outfile)


# MAIN PROGRAM
if __name__ == '__main__':
    # list of urls of makes
    makes = get_makes()

    # list of urls of models
    models = get_models(makes)

    # list of urls of years
    years = get_years(models)

    # list of final urls
    trims = get_trims(years)

    # scrape all urls
    scrape_cars(trims)

    # dump data to json file
    dump_data()
