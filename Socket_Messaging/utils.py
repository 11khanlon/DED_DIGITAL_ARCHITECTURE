import os 

#finding the latest csv file in the folder, which is where the data is being saved

def get_latest_csv(folder):

    #files = [f for f in os.listdir(folder) if f.endswith(".csv")]
    files = []

    for f in os.listdir(folder):

        if f.endswith(".csv"):
            files.append(f)

    if not files:
        return None

    files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)))

    return os.path.join(folder, files[-1])

#folder = r"C:\\Users\\Kayleigh\\DIGITAL_ARCH_REPO\\RPMI_DATA_DEV\\data_csv_examples"   INSERT ACTUAL FILE PATH