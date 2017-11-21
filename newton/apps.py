from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem


class SuitConfig(DjangoSuitConfig):
    menu = (
        # ParentItem('Score It!', children=[
        #     ChildItem('Scores', 'scoreit.scores'),
        #     ChildItem('Classroom Approval', 'scoreit.classroomapproval'),
        # ], icon='fa fa-leaf'),

        # ParentItem('Grade Book', children=[
        #     ChildItem('CCSS', 'gradebook.commoncorestatestandard'), ], icon='fa fa-leaf'),

        ParentItem('Morning Message', children=[
            ChildItem('Messages', 'brain.morningmessage'),
            ChildItem('Settings', 'brain.morningmessagesettings'),
            ChildItem('Class Schedule', 'brain.schedule'),
        ], icon='fa fa-leaf'),

        ParentItem('Stickers', children=[
            ChildItem('Chosen Avatars', 'badges.avatar'),
            ChildItem('Sticker Assignments', 'badges.stickerassignment'),
            ChildItem('Stickers', 'badges.sticker'),
        ], icon='fa fa-leaf'),

        ParentItem('Reading', children=[
            ChildItem('Student Stats', 'brain.readingstats'),
        ], icon='fa fa-leaf'),

        ParentItem('AMC', children=[
            ChildItem('Scores', 'amc.amctestresult'),
            ChildItem('Starting Tests', 'amc.amcstartingtest'),
            ChildItem('Tests', 'amc.amctest'),
        ], icon='fa fa-leaf'),

        ParentItem('CGI', children=[
            ChildItem('Questions', 'mathcgi.cgi'),
            ChildItem('Results', 'mathcgi.cgiresult'),
        ], icon='fa fa-leaf'),

        ParentItem('IXL', children=[
            ChildItem('Challenge Assignments', 'ixl.challengeassignment'),
            ChildItem('Challenges', 'ixl.challenge'),
            ChildItem('Student Stats','ixl.ixlstats')
        ], icon='fa fa-leaf'),

        ParentItem('NWEA', children=[
            ChildItem('Scores','nwea.nweaaverage'),
            ChildItem('Goals', 'nwea.nweagoal'),
            ChildItem('Math Breakdown', 'nwea.nweascore'),
        ]),


        ParentItem('Roster', children=[
            ChildItem('Students', 'brain.studentroster'),
            ChildItem('Classrooms', 'brain.classroom'),
            ChildItem("Student Account Info","brain.accountinfo"),
            ChildItem('Newton User Accounts','auth.user'),
            ChildItem('Grade Groups', 'auth.group'),
        ], icon='fa fa-users'),
    )

    def ready(self):
        super(SuitConfig, self).ready()


SUIT_CONFIG = {
    'ADMIN_NAME': 'Newton Admin',
    'MENU': (
        {'app': 'scoreit', 'label': 'Score It!', 'icon': 'icon-thumbs-up'},
        {'app': 'brain', 'label': 'Core Functions', 'icon': 'icon-leaf'},
        {'app': 'amc', 'label': 'Math | AMC', 'icon': 'icon-time'},
        {'app': 'mathcgi', 'label': 'Math | CGI', 'icon': 'icon-ok'},
        {'app': 'ixl', 'label': 'Math | IXL', 'icon': 'icon-star'},
        {'app': 'nwea', 'label': 'Math | NWEA', 'icon': 'icon-road'},
        # {'app': 'videos', 'label': 'Videos', 'icon': 'icon-facetime-video'},
        {'app': 'auth', 'label': 'Authorization', 'icon': 'icon-lock'},
    ),
}
