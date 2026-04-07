import cv2
import os

# 🔥 GIVE YOUR IMAGE FOLDER PATH HERE
input_folder = r"C:\Users\preet\Desktop\10 Images"   # change this

# ✅ FIX: check if folder exists (ADDED ONLY THIS)
if not os.path.exists(input_folder):
    print("❌ Error: Folder not found ->", input_folder)
    exit()

# Output folders
base_folder = "output"
folders = ["blur", "gray", "edge", "resize"]

for folder in folders:
    os.makedirs(os.path.join(base_folder, folder), exist_ok=True)

# Read all files from folder
files = os.listdir(input_folder)

# Process each file
for file in files:

    # Only process image files
    if not file.lower().endswith((".jpg", ".png", ".jpeg")):
        continue

    img_path = os.path.join(input_folder, file)
    img = cv2.imread(img_path)

    if img is None:
        print(f"❌ Cannot load: {file}")
        continue

    name = os.path.splitext(file)[0]

    # Processing
    blur = cv2.GaussianBlur(img, (15, 15), 0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edge = cv2.Canny(img, 100, 200)
    resize = cv2.resize(img, (300, 300))

    # Save into folders
    cv2.imwrite(os.path.join(base_folder, "blur", f"{name}_blur.jpg"), blur)
    cv2.imwrite(os.path.join(base_folder, "gray", f"{name}_gray.jpg"), gray)
    cv2.imwrite(os.path.join(base_folder, "edge", f"{name}_edge.jpg"), edge)
    cv2.imwrite(os.path.join(base_folder, "resize", f"{name}_resize.jpg"), resize)

    print(f"✅ Processed: {file}")

print("🎉 All images processed from folder!")