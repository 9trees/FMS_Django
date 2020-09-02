import os, csv, ast
from batch.models import *

#this line too works
#print("I'm from Script")

def check_batchFiles(b_path):
    """Checks for batch output files"""
    if os.path.isdir(os.path.join(b_path, 'output')):
        csv_files = []
        imageFileNames =[]
        for root, dirs, files in os.walk(os.path.join(b_path, 'output')):
            for file in files:
                if file.endswith('.jpeg') or file.endswith('.JPG') or file.endswith('.jpg') or file.endswith('.png'):
                    csv_nm = file.split('.')[0] + ".csv"
                    if os.path.exists(os.path.join(root, csv_nm)):
                        print("CSV File available for {}".format(file))
                        csv_files.append(os.path.join(root, csv_nm))
                        imageFileNames.append(file)
                    else:
                        print("No CSV File available for {}".format(file))
        #print("Batch outputs available! {}, {}".format(csv_files, imageFileNames))
        return csv_files, imageFileNames
    else:
        print("Batch output files dose not exist!")
def creatGlobalCSV(csv_files, imageFileNames, b_path):
    """Create Global CSV for specific Batch and update the Image Bank DB Table recodes."""
    gfName = b_path + "\output\global.csv"
    with open(gfName, 'w', newline='') as csvfile:
        fieldnames = ['File Name', 'Sample ID', 'Sample Color', 'Sample Length', 'Sample Diameter']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for cfile, imname in zip(csv_files, imageFileNames):
            with open(cfile, newline='') as csvfile:
                creader = csv.reader(csvfile)
                for row in creader:
                    print(len(row))
            sampleId = ast.literal_eval(row[0])
            sampleCol = ast.literal_eval(row[1])
            sampleLen = ast.literal_eval(row[2])
            sampleDia = ast.literal_eval(row[3])
            for sId, sCol, sLen, sDia in zip(sampleId, sampleCol, sampleLen, sampleDia):
                print(imname, sId, sCol, sLen, sDia)
                writer.writerow({'File Name': imname, 'Sample ID': sId, 'Sample Color': sCol, 'Sample Length': sLen,
                                 'Sample Diameter': sDia})

def update_imgBank(batch_name, b_path):
    """get batch output values and update Image Bank table in DB """
    batch_name = Batch.objects.get(name=batch_name)
    images = ImageBank.objects.filter(batch=batch_name)
    for image in images:
        img_row = ImageBank.objects.get(request_id=image.request_id)
        with open(os.path.join(b_path, 'output', img_row.file_name.split('.')[0] + ".csv"), newline='') as isfile:
            csv_read = csv.reader(isfile)
            for row in csv_read:
                print(len(row))
        sample_id = ast.literal_eval(row[0])
        img_row.no_of_samples = len(sample_id)
        img_row.sample_details = row
        img_row.status = '1'
        img_row.save()
    batch_name.batch_status = '2'
    batch_name.save()
    #print(images)

def run():
    """Main function which handles all the flow"""
    un = str(input("Enter the User.pk Value!\n"))
    bh_name = str(str(input("Enter the Batch Name!\n")))
    b_path = os.path.join(os.getcwd(), 'static', 'data', un, bh_name)
    #print(d_path)
    csv_files, imageFileNames = check_batchFiles(b_path)
    creatGlobalCSV(csv_files, imageFileNames, b_path)
    update_imgBank(bh_name, b_path)

