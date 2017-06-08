from django.conf.urls import url, include

from students.views import students as students_views, groups as groups_views, journal as journal_views, \
    exams as exams_views
from .views.contact_admin import ContactUsView


urlpatterns = [
    # Students urls
    url(r'^students-list/$', students_views.StudentsListView.as_view(), name='students_list'),
    url(r'^students/add/$', students_views.StudentAddView.as_view(), name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$', students_views.StudentsEditView.as_view(), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$', students_views.StudentsDeleteView.as_view(), name='students_delete'),

    # Groups urls
    url(r'^groups/$', groups_views.GroupsListView.as_view(), name="groups_list"),
    url(r'^groups/add/$', groups_views.GroupsAddView.as_view(), name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$', groups_views.GroupsEditView.as_view(), name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$', groups_views.GroupsDeleteView.as_view(), name='groups_delete'),

    # Journal urls
    url(r'^journal/(?P<pk>\d+)?/?$', journal_views.JournalView.as_view(), name="journal"),
    url(r'^journal/(?P<jid>\d+)/$', journal_views.JournalSpecificStudentView.as_view(),
        name="journal_specific_student"),
    url(r'^journal/update/$', journal_views.JournalUpdateView.as_view(), name="journal_update"),

    # Exams List url
    url(r'^exams/$', exams_views.ExamsListView.as_view(), name='exams_list'),
    url(r'^exams-add/$', exams_views.ExamAddView.as_view(), name='exams_add'),
    url(r'^exams-edit/(?P<pk>\d+)/$', exams_views.ExamEditView.as_view(), name='exams_edit'),
    url(r'^exams-delete/(?P<pk>\d+)/$', exams_views.ExamDeleteView.as_view(), name='exams_delete'),
    url(r'^exams-result/(?P<pk>\d+)/$', exams_views.ExamResultView.as_view(), name='exams_results'),

    # Contact admin urls
    url(r'^contact-admin/$', ContactUsView.as_view(), name='contact-admin'),
    # url(r'^contact/', include('contact_form.urls'), name='contact_form'),

]
