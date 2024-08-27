import argparse


def set_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages_to_db_csv_path", type=str, required=True)
    parser.add_argument("--queries_csv_path", type=str, required=True)
    args = parser.parse_args()
    args_dict = vars(args)
    print(args_dict)
    return args_dict




if __name__ == "__main__":
    args_dict = set_args()



