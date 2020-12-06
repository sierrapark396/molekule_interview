import requests
import psycopg2
import json

# change these to use different APIs
url = "https://data.sfgov.org/resource/jjew-r69b.json"
headers = {"X-App-Token": "Jg0wNONuZF8AS1MXBjc5lHJKP"}
params = {}


def request_data_from_api(url: str, params: dict, headers: dict) -> dict:
    """
    Pings the API with the parameters/headers.
    Returns: json data of API
    """

    result = requests.get(url, params=params, headers=headers)
    result_json = result.json()
    return result_json


def load_to_staging(url: str, params: dict, headers: dict) -> bool:
    """
    connect to PostgreSQL and insert data into an existing table
    Returns: boolean
    """
    result = request_data_from_api(url, params, headers)
    conn = psycopg2.connect(
        database="molekule-data",
        user="spark",
        password="",
        host="127.0.0.1",
        port="5432",
    )
    cur = conn.cursor()
    sql_statement = """INSERT INTO stg_food_trucks(
        dayorder,
        dayofweekstr,
        starttime,
        endtime,
        permit,
        location,
        locationdesc,
        optionaltext,
        locationid,
        start24,
        end24,
        cnn,
        addr_date_create,
        addr_date_modified,
        block,
        lot,
        coldtruck,
        applicant,
        x,
        y,
        latitude,
        longitude,
        location_2
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    for record in result:
        cur.execute(
            sql_statement,
            (
                record.get("dayorder", ""),
                record.get("dayofweekstr", ""),
                record.get("starttime", ""),
                record.get("endtime", ""),
                record.get("permit", ""),
                record.get("location", ""),
                record.get("locationdesc", ""),
                record.get("optionaltext", ""),
                record.get("locationid", ""),
                record.get("start24", ""),
                record.get("end24", ""),
                record.get("cnn", ""),
                record.get("addr_date_create", ""),
                record.get("addr_date_modified", ""),
                record.get("block", ""),
                record.get("lot", ""),
                record.get("coldtruck", ""),
                record.get("applicant", ""),
                record.get("x", ""),
                record.get("y", ""),
                record.get("latitude", ""),
                record.get("longitude", ""),
                json.dumps(record.get("location_2", "")),
            ),
        )
    conn.commit()
    return True


def main():
    load_to_staging(url, params, headers)


if __name__ == "__main__":
    main()
