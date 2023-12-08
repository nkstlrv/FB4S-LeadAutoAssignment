from db.postgres import p_queries as postgres


def prepare_postalcode(postalcode: str):
    res = ''
    if len(postalcode) > 0:
        if len(postalcode) == 6:
            res = f"{postalcode[0:3]} {postalcode[3:6]}"
        else:
            res = postalcode
    return res


def get_not_excluded_realtors(city: str, province: str, email_array: list) -> list:
    excluded_emails = []
    for email in email_array:
        excluded_email = postgres.get_excluded_cities_by_city_province_emails(city, province, email)
        if len(excluded_email) > 0: excluded_emails.append(excluded_email[0][3])
    not_excluded_emails = [email for email in email_array if email not in excluded_emails]
    return not_excluded_emails


if __name__ == "__main__":
    get_not_excluded_realtors(
        city="Hanover",
        province="Ontario",
        email_array=['Manoj@MoveWithManoj.ca', 'nikita.stoliarov+1@actse.ltd']
    )