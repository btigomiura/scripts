"""Script for creating a timeseries csv file."""

import argparse
import csv
import datetime
import os
import random
from typing import Tuple, List, Dict

DATETIME_FORMAT = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')


def parse_command_line_arguments() -> Tuple[int, int, int, str, int]:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num-records",
        default="500",
        type=int,
        help="Number of records.",
    )
    parser.add_argument(
        "--first-data-timestamp",
        default=1648785596000,
        type=int,
        help="Timestamp of the first data. Should be epoch time im milliseconds.",
    )
    parser.add_argument(
        "--data-interval",
        default=1,
        type=int,
        help="Data interval in seconds.",
    )
    parser.add_argument(
        "--file-path",
        default=f"{os.getcwd()}/{DATETIME_FORMAT}_created_timeseries.csv",
        type=str,
        help="Output file path of created csv file."
    )
    parser.add_argument(
        "--num-columns",
        default=5,
        type=int,
        help="Number of columns."
    )
    args = parser.parse_args()

    return (
        args.num_records,
        args.first_data_timestamp,
        args.data_interval,
        args.file_path,
        args.num_columns
    )


def create_file_content(
    num_records: int, first_data_timestamp: int, data_interval: int, num_columns: int
) -> Tuple[List[str], List[Dict[str, int]]]:
    """Returns the field names and field values."""
    field_names = [f"col_{idx}" for idx in range(num_columns - 1)]

    def _create_dict(idx: int):
        ret_val = {
            key: 500 + random.uniform(-10, 10)
            for key in field_names
        }
        ret_val["Timestamp"] = first_data_timestamp + idx * data_interval * 1000
        return ret_val

    field_values = [
        _create_dict(idx)
        for idx in range(num_records)
    ]

    field_names = ["Timestamp"] + field_names

    return field_names, field_values


def write_csv(
    file_path: str, field_names: List[str], field_values: List[Dict[str, int]]
) -> None:
    """Create csv file."""
    with open(file_path, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(field_values)


def main():
    """Main function."""
    (
        num_records,
        first_data_timestamp,
        data_interval,
        file_path,
        num_columns
    ) = parse_command_line_arguments()

    field_names, field_values = create_file_content(
        num_records, first_data_timestamp, data_interval, num_columns
    )

    write_csv(file_path, field_names, field_values)


if __name__ == "__main__":
    main()
