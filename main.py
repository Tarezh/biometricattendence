import os
import cv2
from tkinter import filedialog, Tk, messagebox
import csv
from datetime import datetime

# sample = cv2.imread("sample iamge address")

root = Tk()
root.withdraw()  # Hide the main window
sample_path = filedialog.askopenfilename(title="Select Sample Image", filetypes=[("Image files", "*.png;*.jpg;*.bmp")])

# Check if the user selected a file
if not sample_path:
    print("Error: No sample image selected.")
    exit()

sample = cv2.imread(sample_path)

# Check if the sample image is loaded successfully
if sample is None:
    print("Error: Unable to load the sample image.")
    exit()

# cv2.imshow("Sample", sample)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

best_score = 0
filename = None
image = None
kp1, kp2, mp = None, None, None

for file in [file for file in os.listdir("fingerprint_images")][:1000]:
    # print(file)
    fingerprint_image = cv2.imread("fingerprint_images/" + file)
    sift = cv2.SIFT_create()
    # print(sift)
    keypoints_1, descriptors_1 = sift.detectAndCompute(sample, None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_image, None)

    matches = cv2.FlannBasedMatcher({'algorithm' : 1, 'trees' : 10}, {}).knnMatch(descriptors_1, descriptors_2, k=2)
    match_points = []

    for p, q in matches:
        if p.distance < 0.1*q.distance:
            match_points.append(p)
    # print(match_points)
    keypoints = 0
    if len(keypoints_1) < len(keypoints_2):
        keypoints = len(keypoints_1)
    else:
        keypoints = len(keypoints_2)

    if len(match_points) / keypoints * 100 > best_score:
        best_score = len(match_points) / keypoints * 100
        filename = file
        image = fingerprint_image
        kp1, kp2, mp = keypoints_1, keypoints_2, match_points
        result = cv2.drawMatches(sample, kp1, fingerprint_image, kp2, mp, None)

print("BEST MATCH: " + str(filename))
# print("SCORE:" + str(best_score))

csv_file_path = 'recognized_fingerprints.csv'
fields = ['File', 'Date']

def mark_attendance(filename):
    messagebox.showinfo("Attendance Marked", f"Attendance marked for {filename}")


attendance_marked = False

with open(csv_file_path, 'r', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    
    for row in csv_reader:
        if row and row[0] == filename:  # Assuming the filename is in the first column
            attendance_marked = True
            break

if attendance_marked:
    messagebox.showinfo("Attendance Already Marked", f"Attendance already marked for {filename}")
elif best_score != 0:
    mark_attendance(filename)
    with open(csv_file_path, 'a', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=fields)
        csv_writer.writerow({'File': filename, 'Date': datetime.now().strftime("%Y-%m-%d")})
else:
    messagebox.showinfo("Error", f"No Match Found Try Again!")

# cv2.resize(result, None, fx = 4, fy = 4)
# cv2.imshow("Result", result)

# cv2.waitKey(0)

# cv2.destroyAllWindows()

