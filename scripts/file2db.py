import os, csv, json
from batch.models import *


# this line too works
# print("I'm from Script")

def check_batch_files(b_path):
    """Checks for batch output files"""
    if os.path.isdir(os.path.join(b_path, 'output')):
        csv_files = []
        # imageFileNames =[]
        for root, dirs, files in os.walk(os.path.join(b_path, 'output')):
            for file in files:
                if file.endswith('.jpeg') or file.endswith('.JPG') or file.endswith('.jpg') or file.endswith('.png'):
                    csv_nm = file.split('.')[0] + ".csv"
                    if os.path.exists(os.path.join(root, csv_nm)):
                        print("CSV File available for {}".format(file))
                        csv_files.append(os.path.join(root, csv_nm))
                        # imageFileNames.append(file)
                    else:
                        print("No CSV File available for {}".format(file))
        # print("Batch outputs available! {}, {}".format(csv_files, imageFileNames))
        return csv_files
    else:
        print("Batch output files dose not exist!")


def create_global_csv(csv_files, b_path):
    """Create Global CSV for specific Batch and update the Image Bank DB Table recodes."""
    gfName = b_path + "\output\global.csv"
    with open(gfName, 'w', newline='') as csvfile:
        fieldnames = ['File Name', 'Sample ID', 'Sample Color', 'Sample Length', 'Sample Diameter']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for cfile in csv_files:
            img_name = []
            sample_id = []
            sample_col = []
            sample_len = []
            sample_dia = []
            with open(cfile, newline='') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    print(len(row))
                    img_name.append(row[0])
                    sample_id.append(row[1])
                    sample_col.append(row[2])
                    sample_len.append(row[3])
                    sample_dia.append(row[4])
            for img, sId, sCol, sLen, sDia in zip(img_name, sample_id, sample_col, sample_len, sample_dia):
                print(img, sId, sCol, sLen, sDia)
                writer.writerow({'File Name': img, 'Sample ID': sId, 'Sample Color': sCol, 'Sample Length': sLen,
                                 'Sample Diameter': sDia})


def update_img_bank(batch_name, b_path, un):
    """get batch output values and update Image Bank table in DB """
    bh_name = batch_name
    batch_name = Batch.objects.get(name=batch_name)
    images = ImageBank.objects.filter(batch=batch_name)
    fieldnames = ("FN", "SID", "SCOL", "SLEN", "SDIA")
    for image in images:
        img_row = ImageBank.objects.get(request_id=image.request_id)
        with open(os.path.join(b_path, 'output', img_row.file_name.split('.')[0] + ".csv"), newline='') as csv_file:
            reader = csv.DictReader(csv_file, fieldnames)
            data = json.dumps([row for row in reader])

        rdata = json.loads(data)
        img_row.no_of_samples = len(rdata)
        img_row.sample_details = data
        img_row.URL = "data/" + str(un) + "/" + bh_name + "/" + "output/" + img_row.file_name
        img_row.status = '1'
        img_row.save()
    batch_name.batch_status = '2'
    batch_name.save()
    # print(images)


def run():
    """Main function which handles all the flow"""
    un = str(input("Enter the User.pk Value!\n"))
    bh_name = str(str(input("Enter the Batch Name!\n")))
    b_path = os.path.join(os.getcwd(), 'static', 'data', un, bh_name)
    # print(d_path)
    csv_files = check_batch_files(b_path)
    create_global_csv(csv_files, b_path)
    update_img_bank(bh_name, b_path, un)
