# #Core Django imports
# from django.test import TestCase
#
#
# #Third-party app imports
# from model_mommy import mommy
# from model_mommy.recipe import Recipe, foreign_key
#
# # Relative imports of the 'app-name' package
# from brain.models import Classroom, StudentRoster, School, SchoolDay, Schedule, CurrentClass, AccountInfo, BehaviorReport
#
# class StudentRosterModelTests(TestCase):
#     """
#     Class to test the model
#     Kid
#     """
#
#     def setUp(self):
#         """
#         Set up all the tests
#         """
#         self.user = mommy.make('User')
#         self.school = mommy.make('School', id=2)
#         self.classroom = mommy.make('Classroom', _quantity=4)
#         self.currentclass = mommy.make('CurrentClass', _quantity=4)
#         self.student = mommy.make('StudentRoster', _quantity=20)
#         self.accountinfo = mommy.make('AccountInfo')
#
#
#     def test_classroom_create(self):
#         self.assertIn(self.classroom, Classroom.objects.all())
#
# class StudentRosterModelTests(TestCase):
#
#     def setUp(self):
#         self.classroom = Classroom.objects.create(title = 'MR', first_name ="Eugene", last_name="Tesclassroom")
#         self.current_class = CurrentClass.objects.create(year = 16-17, grade = "SECOND", classroom= self.classroom )
#         self.student = StudentRoster.objects.create(first_name="Steve", last_name="Tester", date_of_birth="2008-3-3",
#                                                     current_class= self.current_class
#                                                     )
#
#     def test_classroom_create(self):
#         self.assertIn(self.classroom, Classroom.objects.all())
#
#     def test_class_create(self):
#         self.assertIn(self.current_class, CurrentClass.objects.all())
#
#
#     def test_student_create(self):
#         #student = StudentRoster.objects.create(first_name = "John", last_name = "Doe", gender = "MALE", email = "Dan@gmail.com",)
#         self.assertIn(self.student, StudentRoster.objects.all())
#
#
# class StudentRosterViewsTests(TestCase):
#
#     def setUp(self):
#         self.classroom = Classroom.objects.create(title = 'MR', first_name ="Eugene", last_name="Tesclassroom")
#         self.current_class = CurrentClass.objects.create(year = 16-17, grade = "SECOND", classroom= self.classroom )
#         self.student = StudentRoster.objects.create(first_name="Steve", last_name="Tester", date_of_birth="2008-3-3",
#                                                     current_class= self.current_class
#                                                     )
#     def test_student_in_schoolroster(self):
#         resp = self.client.get(reverse('brain:schoolroster', args=[self.current_class.year]))
#         self.assertEqual(resp.status_code, 200)
#         self.assertIn(self.student, resp.context['student_list'])
#         self.assertTemplateUsed(resp, 'brain/year_list.html')
#         self.assertContains(resp, self.student.last_name)
#
#     def test_student_in_gradelist(self):
#         resp = self.client.get(reverse('brain:gradelist', args=[self.current_class.year, self.current_class.grade]))
#         self.assertEqual(resp.status_code, 200)
#         self.assertIn(self.student, resp.context['student_list'])
#         self.assertTemplateUsed(resp, 'brain/grade_list.html')
#         self.assertContains(resp, self.student.last_name)
#
#     def test_student_in_classlist(self):
#         resp = self.client.get(reverse('brain:classlist', args=[self.current_class.year, self.current_class.grade, self.current_class.classroom.last_name]))
#         self.assertEqual(resp.status_code, 200)
#         self.assertIn(self.student, resp.context['student_list'])
#         self.assertTemplateUsed(resp, 'brain/class_list.html')
#         self.assertContains(resp, self.student.last_name)
#
#     def test_student_in_student_detail(self):
#         resp = self.client.get(reverse('brain:studentdetail', args=[self.student.student_id]))
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(self.student, resp.context['student'])
#         self.assertTemplateUsed(resp, 'brain/student_detail.html')
#         self.assertContains(resp, self.student.last_name)
#
