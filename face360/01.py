import face_recognition

def findFace(image):
    face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model='cnn')
    top, right, bottom, left = face_locations[0]
    return image[top:bottom, left:right]


jobs_image = face_recognition.load_image_file('.\\src\\我.jpg')
print(jobs_image)

# face_locations = face_recognition.face_locations(jobs_image, number_of_times_to_upsample=0, model='cnn')
# top, right, bottom, left = face_locations[0]
# face_image = jobs_image[top:bottom, left:right]
# cv2.imshow('11111', face_image)
# cv2.waitKey(0)
# obama_image = face_recognition.load_image_file(".\\src\\obama.jpg")
# wo_image = face_recognition.load_image_file(".\\src\\我.jpg")
unknown_image = face_recognition.load_image_file('E:\\pythonDemo\\face360\\tmp\\2.jpg')

jobs_encoding = face_recognition.face_encodings(jobs_image)[0]
# obama_encoding = face_recognition.face_encodings(obama_image)[0]
# wo_encoding = face_recognition.face_encodings(wo_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([jobs_encoding], unknown_encoding)

print(results)

# labels = ['jobs', 'obama', 'wo']
#
# print('results:' + str(results))
#
# for i in range(0, len(results)):
#     if results[i]:
#         print('The person is:' + labels[i])
