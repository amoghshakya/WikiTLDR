import time
import sys

import wikipedia    # type: ignore
from fetch_wikipedia import fetch_summaries
from queries import init_database, insert_articles


def build_dataset(num_articles: int = 10000, batch_size: int = 50, output_file: str = r"out.db"):
    conn = init_database(output_file)

    # set language to simple English
    wikipedia.set_lang("simple")

    batch: list[dict] = []
    batch_count = 0

    for _ in range(num_articles):
        article = wikipedia.random()
        print(f"Fetching {article}")

        input_text = fetch_summaries(article, lang="en")
        target_text = fetch_summaries(article, lang="simple")

        if not input_text:
            print(f"Skipping {article} due to issues.")
            continue

        batch.append(dict(
            title=article,
            input_text=input_text,
            target_text=target_text,
        ))

        # push to db if batch_size is full
        if len(batch) >= batch_size:
            insert_articles(conn, batch)
            print(f"Batch {batch_count + 1} inserted into the database.")
            batch = []
            batch_count += 1

        time.sleep(1)

    if batch:
        insert_articles(conn, batch)
        print(f"Final batch written to {output_file}")


if __name__ == "__main__":
    try:
        if len(sys.argv) <= 2:
            print(f"Usage: {sys.argv[0]} <num_titles> <batch_size> <db_name>")
            sys.exit(1)

        num_titles = int(sys.argv[1])
        batch_size = int(sys.argv[2])
        db_name = sys.argv[3]

        dataset = build_dataset(num_titles, batch_size, db_name)
    except:
        print(f"Usage: {sys.argv[0]} <num_titles> <batch_size> <db_name>")
