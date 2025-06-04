import argparse
from .gui import get_user_input
from .recommender import MovieRecommender


def main() -> None:
    parser = argparse.ArgumentParser(description="Movie recommendation demo")
    parser.add_argument(
        "--movies",
        help="Comma separated list of liked movie titles. If omitted the GUI launches.",
    )
    parser.add_argument(
        "--top", type=int, default=30, help="Number of recommendations to display"
    )
    args = parser.parse_args()

    if args.movies:
        recommender = MovieRecommender()
        titles = [m.strip() for m in args.movies.split(",") if m.strip()]
        for rec in recommender.recommend(titles, top_n=args.top):
            print(rec)
    else:
        get_user_input()


if __name__ == "__main__":
    main()
