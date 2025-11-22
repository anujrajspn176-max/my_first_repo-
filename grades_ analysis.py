 import numpy as np

 grades = np.random.randint(80, 100, size=(5, 5))
 print(grades)

 subject_avg = np.mean(grades, axis=0)
 student_avg = np.mean(grades, axis=1)

 subject_max = np.max(grades, axis=0)
 student_min = np.min(grades, axis=1)

 print("subject_avg:", subject_avg)
 print("student_avg:", student_avg)

 print("subject_max:", subject_max)
 print("student_min:", student_min)