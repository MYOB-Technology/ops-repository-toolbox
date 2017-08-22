from toolbox.people import retrieve_users, retrieve_user_details
import csv

def write_csv_detail_retrieved(args, filename, keys, input_content):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', dialect='excel')
        writer.writerow(key for key in keys)
        for item in input_content:
            content_dict = item
            writer.writerow(content_dict[key] for key in keys)
