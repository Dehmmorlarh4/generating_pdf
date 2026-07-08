#!/usr/bin/env python3

import json

import sys

from collections import Counter

import reports

import emails


def load_data(filename):

    """Loads the contents of filename as a JSON file."""

    with open(filename) as json_file:

        data = json.load(json_file)

    return data


def format_car(car):

    """Given a car dictionary, returns a nicely formatted name."""

    return "{} {} ({})".format(

        car["car_make"],

        car["car_model"],

        car["car_year"]

    )


def process_data(data):

    """Analyzes the data and returns summary lines."""

    max_revenue = {"revenue": 0}

    max_sales = {"total_sales": 0}

    year_sales = Counter()

    for item in data:

        # Revenue

        price = float(item["price"].replace("$", "").replace(",", ""))
        revenue = price * item["total_sales"]

        if revenue > max_revenue["revenue"]:

            item["revenue"] = revenue

            max_revenue = item

        # Most sales

        if item["total_sales"] > max_sales["total_sales"]:

            max_sales = item

        # Popular year

        year_sales[item["car"]["car_year"]] += item["total_sales"]

    popular_year, sales = year_sales.most_common(1)[0]

    summary = [

        "The {} generated the most revenue: ${:,.2f}".format(

            format_car(max_revenue["car"]),

            max_revenue["revenue"]

        ),

        "The {} had the most sales: {}".format(

            format_car(max_sales["car"]),

            max_sales["total_sales"]

        ),

        "The most popular year was {} with {} sales.".format(

            popular_year,

            sales

        )

    ]

    return summary

def cars_dict_to_table(car_data):

    """Turns JSON data into table data."""

    table_data = [["ID", "Car", "Price", "Total Sales"]]

    car_data.sort(key=lambda x: x["id"])

    for item in car_data:

        table_data.append([

            item["id"],

            format_car(item["car"]),

            item["price"],

            item["total_sales"]

        ])

    return table_data

def main(argv):

    data = load_data("car_sales.json")

    summary = process_data(data)

    pdf_path = "/tmp/cars.pdf"

    reports.generate(

        pdf_path,

        "Sales summary for last month",

        "\n".join(summary),

        cars_dict_to_table(data)

    )

    message = emails.generate(

        sender="automation@example.com",

        recipient="student@example.com",

        subject="Sales summary for last month",

        body="\n".join(summary),

        attachment_path=pdf_path

    )

    emails.send(message)


if __name__ == "__main__":

    main(sys.argv)
