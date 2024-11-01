import face_recognition
import numpy as np
from datetime import datetime
import os
import cv2
import keyboard
import pyautogui
import customtkinter as cstk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image
import threading
import winsound

path = "ImagesAttendance"
attend_csv_path = r"Attendance.csv"
cstk.set_appearance_mode("dark")
cstk.set_default_color_theme("green")
root = cstk.CTk()
root.geometry("1920x1080")
root.title("Bus check in system using facial recognition")
path_Minh = os.getcwd()
images = []
global image_ids
global filesz
global encodeList
encodeList=[]
filesz=tuple()
image_ids = []  
mylist = os.listdir(path)  
savedImg = []
global attend_dict
attend_dict={}
global del_names,del_ind
del_names=[]
del_ind=[]

def access():
    global images,image_ids
    for cl in mylist:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        image_ids.append(os.path.splitext(cl)[0]) 
    print(image_ids)

def find_encodings(images):
    encodeList = []
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(image)
        if encodings:  # Check if the list is not empty
            encode = encodings[0]
            encodeList.append(encode)
        else:
            print("No face found in the image")
    return encodeList
# lưu ảnh quét
# def save_img(imagesz,nami):
#     savedImg=os.listdir(only_name)
#     if nami not in savedImg:
#         cv2.imwrite(rf"{only_name}+\{nami}.jpg", imagesz)
def markAttendance(id):
    with open("Attendance.csv", 'r+') as f:
        myDataList = f.readlines() 

        for line in myDataList:
            line = line.strip()
            entry = line.split(',')
            attend_dict[entry[0]] = entry[1:]
        if id not in attend_dict.keys():
            now = datetime.now()
            tString = now.strftime("%I:%M %p")  # lay gio
            dString = now.strftime("%d/%m/%Y")  # lay ngay
            attend_dict[id] = [tString,""]  # writes time
            attend_dict[id][1] = dString  # writes date
            winsound.Beep(1000, 800)
def open_attendance():
    os.startfile(r"Attendance.csv")
def webcam_scan():
    cap = cv2.VideoCapture(0) # starts video capture through webcam
     # Thiết lập kích thước khung hình
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Chiều rộng
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)  # Chiều cao

    while True:
        # img = numpy array  ,  succces= if loaded or not
        success, img = cap.read()
        # giảm kích thức đi 4 lần để tính cho lẹ
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        # hong có mặt thằng nào hết
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

        # này nhận diện nè
        for encodeFace,FaceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace,tolerance=0.5)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            matchIndex = np.argmin(faceDis) # matchIndex là chỉ mục của ảnh nhận diện được trong toàn bộ ảnh

            if matches[matchIndex]:
                id = image_ids[matchIndex]
                # print(name)
                # FaceLoc = up right down left
                y1,x2,y2,x1=FaceLoc
                # nhân lên 4 lần lại vì nãy giảm 4 lần
                # sau đó vẽ lên hình kích thước ban đầu
                y1, x2, y2, x1=y1*4,x2*4,y2*4,x1*4

                # vẽ hình vuôn quanh khuôn mặt
                cv2.rectangle(img, (x1,y1),(x2,y2) ,(255, 255, 0), 2)
                cv2.rectangle(img, (x1, y2-35), (x2, y2),(255, 255, 0), cv2.FILLED)
                # hiện id
                cv2.putText(img, id, (x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,255), 2)

                markAttendance(id)
                

            else:
                id = "UNKNOWN"
                # FaceLoc = up right down left
                y1, x2, y2, x1 = FaceLoc
                # nhân lên 4 lần lại vì nãy giảm 4 lần
                # sau đó vẽ lên hình kích thước ban đầu
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

                # vẽ hình vuôn quanh khuôn mặt
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 255, 0), cv2.FILLED)
                # hiện id
                cv2.putText(img, id, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)

        # luôn hiện
        cv2.imshow('webcam',img)
        cv2.waitKey(1)
        
        # ấn e để xuất excel
        if keyboard.is_pressed('e'):
            open_attendance()
        # ấn q để dừng
        if keyboard.is_pressed('q'):
            cv2.destroyWindow('webcam')
            attendance()
            break

def attendance():
    ff = open("Attendance.csv", 'w+')
    ss = ""
    try:
        ff.writelines("ID,ENTRY_TIME,ENTRY_DATE")
        ff.writelines("\n")
        del attend_dict['ID']
        del attend_dict['UNKNOWN']
    except KeyError:
        print()

    for i in (attend_dict.keys()):
        ss += i
        entry_time=attend_dict[i][0]
        entry_date=attend_dict[i][1]
        try:
            ss += "," + entry_time + ',' + entry_date
            ff.writelines(ss)
            ff.writelines("\n")
        except ValueError:
            print()

        ss = ""

    ff.close()
#chụp ảnh mới
def take_a_pic():
    new_id = pyautogui.prompt('Enter ID', title="ID")
    if new_id in del_names:
        loc = del_ind[del_names.index(new_id)]
        image_ids[loc] = new_id
        new_id += ".jpg"
        messagebox.showinfo("Alert", "Look at the Camera in 3 sec !")
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Cannot open camera")
            return
        
        result, new_img = cap.read()
        cap.release()
        
        if not result:
            messagebox.showerror("Error", "Failed to capture image")
            return
        
        cv2.imwrite(rf"ImagesAttendance\{new_id}", new_img)
        cv2.imshow("New Image", new_img)
        cv2.waitKey(0)
        cv2.destroyWindow('New Image')
    else:
        new_id += ".jpg"
        messagebox.showinfo("Alert", "Look at the Camera in 3 sec!")
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Cannot open camera")
            return
        
        result, new_img = cap.read()
        cap.release()
        
        if not result:
            messagebox.showerror("Error", "Failed to capture image")
            return
        
        cv2.imwrite(rf"ImagesAttendance\{new_id}", new_img)
        cv2.imshow("New Image", new_img)
        cv2.waitKey(0)
        cv2.destroyWindow('New Image')
        
        images.append(cv2.imread(fr'ImagesAttendance\{new_id}'))
        image_ids.append(os.path.splitext(new_id)[0])
        print(os.path.splitext(new_id)[0])
        encodeList.append(face_recognition.face_encodings(images[-1])[0])

def start_take_a_pic_thread():
    pic_thread = threading.Thread(target=take_a_pic)
    pic_thread.start()
def open_images_to_delete():
    L1 = image_ids
    L2 = []
    li2 = os.listdir(r"ImagesAttendance")
    filesz = filedialog.askopenfilenames(title = "Select image files", filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    print("Selected files:", filesz)
    for xx in filesz:
        os.remove(xx)
        xx = os.path.splitext(xx[xx.find('nce') + 4:])[0]
        #set_dif.append(os.path.splitext(xx)[0])
        del_ind.append(L1.index(xx))
        del_names.append(image_ids[L1.index(xx)])
        image_ids[L1.index(xx)] = "unknown"
        print("removed : ", xx)
    set_dif = []
    for x in li2:
        L2.append(os.path.splitext(x)[0])
    set_dif = list(set(L1).symmetric_difference(set(L2)))
    set_dif = list(filter(lambda t: t != "unknown", set_dif))
    removed_names = ""
    for j in set_dif:
        removed_names += j + " , "
    messagebox.showinfo("showinfo", f"Faces removed = {len(set_dif)}\n{removed_names}\nClose the Window")
def delete_a_face():
    root1 = tk.Toplevel()
    root1.geometry("310x220")
    root1.title("delete")
    path = os.getcwd()
    image_path = os.path.join(path, "other_files", "bg4.png")
    bg1label = tk.Label(root1, image=image_path, width=300, height=180)
    bg1label.pack()
    button9 = tk.Button(root1, text="Select the images", command=open_images_to_delete, width=300,pady=5)
    button9.pack()
    root1.mainloop()
def know_faces():
    os.startfile(r"ImagesAttendance")
#############----Mainn-------#############
if __name__ == "__main__":

    access() # lấy id hình
    encodeListKnown = find_encodings(images) # mã hóa ảnh
    print("Encoding Completed..")
    pil_image = Image.open(os.path.join(path_Minh,"other_files", "bg4.png"))
    imag = cstk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(1080, 1080))

    frame = cstk.CTkFrame(master=root)
    frame.pack(padx=60,pady=20,fill="both",expand=True)

    label = cstk.CTkLabel(master=frame,text="BUS CHECK IN SYSTEM",font=("Roboto",24),compound="left")
    label.pack(pady=12,padx=10)

    bglabel = cstk.CTkLabel(master=frame,image=imag,text="", width=1080,height=1080)
    bglabel.pack()

    button1 = cstk.CTkButton(master=frame,text="Scan face (Webcam)",command=webcam_scan,height=80,width=250,font=("Arial",24))
    button1.place(relx=0.5,rely=0.3,anchor="center")

    button2 = cstk.CTkButton(master=frame,text="Add a new face",command=start_take_a_pic_thread,height=80,width=250,font=("Arial",24))
    button2.place(relx=0.5,rely=0.5,anchor="center")

    button3 = cstk.CTkButton(master=frame,text="Open Attendance",command=attendance,height=80,width=250,font=("Arial",24))
    button3.place(relx=0.5,rely=0.7,anchor="center")

    # button4 = cstk.CTkButton(master=frame,text="Known Images",command=know_faces,height=80,width=250,font=("Arial",24))
    # button4.place(relx=0.75,rely=0.3,anchor="w")
    root.mainloop()

