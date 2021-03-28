from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect

from App_Attendance.forms import AttendanceForm
from App_Attendance.models import *
from App_Login.forms import *
from App_Login.models import *
from datetime import date
import cv2
import face_recognition
import os
import numpy as np


# Create your views here.
@login_required
def index(request):
    studentForm = CreateStudentForm()
    try:
        faculty = request.user.faculty
    except:
        faculty = None
    if faculty:
        teacherForm = FacultyForm(instance=faculty)
        if request.method == 'POST' and 'teacher_submit' in request.POST:
            teacherForm = FacultyForm(request.POST, request.FILES, instance=faculty)
            if teacherForm.is_valid():
                teacherForm.save()
                return HttpResponseRedirect(reverse('App_Attendance:Home'))

    else:
        teacherForm = None
    if request.method == 'POST' and 'student_submit' in request.POST:
        studentForm = CreateStudentForm(request.POST, request.FILES)
        if studentForm.is_valid():
            studentForm.save()
            return HttpResponseRedirect(reverse('App_Attendance:Home'))
    return render(request, 'App_Attendance/home.html',
                  context={'teacher_form': teacherForm, 'student_form': studentForm})


# Student Recognizer
def recognizer(details):
    video = cv2.VideoCapture(0)

    known_face_encodings = []
    known_face_names = []

    # base_dir = os.path.dirname(os.path.abspath(__file__))
    # image_dir = os.path.join(base_dir, "static")
    # image_dir = os.path.join(image_dir, "profile_pics")

    # base_dir = os.getcwd()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # os.chdir("..")
    base_dir = os.getcwd()
    image_dir = f"media/Student_Images/{details['department']}/{details['batch']}/{details['section']}"
    # print(image_dir)
    names = []

    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith('jpg') or file.endswith('png'):
                path = os.path.join(root, file)
                img = face_recognition.load_image_file(path)
                label = file[:len(file) - 4]
                img_encoding = face_recognition.face_encodings(img)[0]
                known_face_names.append(label)
                known_face_encodings.append(img_encoding)

    face_locations = []
    face_encodings = []

    while True:

        check, frame = video.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []

        for face_encoding in face_encodings:

            matches = face_recognition.compare_faces(known_face_encodings, np.array(face_encoding), tolerance=0.6)

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

            try:
                matches = face_recognition.compare_faces(known_face_encodings, np.array(face_encoding), tolerance=0.6)

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    face_names.append(name)
                    if name not in names:
                        names.append(name)
            except:
                pass

        if len(face_names) == 0:
            for (top, right, bottom, left) in face_locations:
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # cv2.rectangle(frame, (left, bottom - 30), (right,bottom - 30), (0,255,0), -1)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, 'Unknown', (left, top), font, 0.8, (255, 255, 255), 1)
        else:
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                # cv2.rectangle(frame, (left, bottom - 30), (right,bottom - 30), (0,255,0), -1)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left, top), font, 0.8, (255, 255, 255), 1)

        cv2.imshow("Face Recognition Panel", frame)

        if cv2.waitKey(1) == ord('e'):
            break

    video.release()
    cv2.destroyAllWindows()
    return names


@login_required
def take_attendance(request):
    form = AttendanceForm()
    context = {'form': form}
    if request.method == 'POST':
        form = AttendanceForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data.get('course'))
            details = {
                'faculty': request.user.faculty,
                'department': form.cleaned_data.get('department'),
                'course': form.cleaned_data.get('course'),
                'batch': form.cleaned_data.get('batch'),
                'section': form.cleaned_data.get('section')
            }
            if Attendance.objects.filter(date=str(date.today()), department=details['department'],
                                         course=details['course'], batch=details['batch'],
                                         section=details['section']).count() != 0:
                messages.error(request, "Attendance already recorded.")
                return redirect('home')
            else:
                students = Student.objects.filter(department=details['department'], batch=details['batch'],
                                                  section=details['section'])
                names = recognizer(details)
                for student in students:
                    if str(student.class_id) in names:
                        attendance = Attendance(Faculty_Name=request.user.faculty,
                                                Student_ID=str(student.class_id),
                                                department=details['department'],
                                                course=details['course'],
                                                batch=details['batch'],
                                                section=details['section'],
                                                status='Present')
                        attendance.save()
                    else:
                        attendance = Attendance(Faculty_Name=request.user.faculty,
                                                Student_ID=str(student.class_id),
                                                department=details['department'],
                                                course=details['course'],
                                                batch=details['batch'],
                                                section=details['section'])
                        attendance.save()
                attendances = Attendance.objects.filter(date=str(date.today()), department=details['department'],
                                                        course=details['course'],
                                                        batch=details['batch'], section=details['section'])
                context = {"attendances": attendances, "ta": True}
                messages.success(request, "Attendance taking Success")
                return HttpResponseRedirect(reverse('App_Attendance:Home'))
    return render(request, 'App_Attendance/attendance.html', context)
