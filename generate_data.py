import json
import random
import uuid
from datetime import datetime, timedelta


def generate_messy_retail_data(base_records=500):
    data = []

    store_ids = [
        "STORE_001",
        "STORE_002",
        "STORE_003",
        "STORE_004",
        "STORE_005"
    ]

    product_ids = [
        "PROD_100",
        "PROD_200",
        "PROD_300",
        "PROD_400",
        "PROD_500"
    ]

    # Generate valid records
    for _ in range(base_records):
        record = {
            "transaction_id": str(uuid.uuid4()),
            "product_id": random.choice(product_ids),
            "store_id": random.choice(store_ids),
            "raw_price": round(random.uniform(10.0, 500.0), 2),
            "transaction_date": (
                datetime.now() -
                timedelta(days=random.randint(0, 14))
            ).strftime("%Y-%m-%d %H:%M:%S")
        }

        data.append(record)

    # Inject missing store_ids
    for i in random.sample(range(base_records), int(base_records * 0.10)):
        data[i]["store_id"] = None

    # Inject negative prices
    for i in random.sample(range(base_records), int(base_records * 0.10)):
        data[i]["raw_price"] = -abs(data[i]["raw_price"])

    # Inject duplicates
    duplicates = random.sample(data, int(base_records * 0.15))
    data.extend(duplicates)

    random.shuffle(data)

    output_filename = "data/raw/messy_raw_pos_data.json"

    with open(output_filename, "w") as f:
        json.dump(data, f, indent=4)

    print(
        f"Successfully generated {len(data)} messy retail records."
    )

    print(
        f"File saved as: {output_filename}"
    )


if __name__ == "__main__":
    generate_messy_retail_data()