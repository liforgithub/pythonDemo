import face_recognition

jobs_image = face_recognition.load_image_file("jobs.jpg")
obama_image = face_recognition.load_image_file("obama.jpg")
wo_image = face_recognition.load_image_file("我.jpg")
unknown_image = face_recognition.load_image_file("un4.jpg")

jobs_encoding = face_recognition.face_encodings(jobs_image)[0]
obama_encoding = face_recognition.face_encodings(obama_image)[0]
wo_encoding = face_recognition.face_encodings(wo_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([jobs_encoding, obama_encoding, wo_encoding], unknown_encoding)
labels = ['jobs', 'obama', 'wo']

print('results:' + str(results))

for i in range(0, len(results)):
    if results[i]:
        print('The person is:' + labels[i])
