import decimal
import traceback


def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            pass


def input_choice(prompt):
    while True:
        try:
            x = input(prompt)
            if x.upper() in ("X", "B"):
                return x.lower()
            return decimal.Decimal(x)
        except decimal.InvalidOperation:
            pass


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        name = input("Name:")
        pages = input_int("Number of pages:")
        if pages <= 0:
            raise ValueError("Expected a number of pages higher than 0.")
        ratings = [decimal.Decimal(0)] * pages
        excluded = [False] * pages
        page = 0
        while page != pages:
            ch = input_choice(f"Page {page + 1}:")
            if ch == "x":
                excluded[page] = True
            elif ch == "b":
                page -= 2
            else:
                ratings[page] = ch
                excluded[page] = False
            page += 1
        rating = decimal.Decimal(
            sum(
                ratings[x] for x in range(pages) if not excluded[x]
            )) / decimal.Decimal(
            pages - excluded.count(True)
        )
        print(
            f"For a hentai of {pages} pages, and {excluded.count(True)} excluded {'pages' if excluded.count(True) != 1 else 'page'}, the rating for {name} is {round(rating,2)}⭐/10⭐")
        input("Press enter to terminate the program.")
    except BaseException as e:
        traceback.print_exc()
        input("Press enter to terminate the program.")
