# blue prints are imported 
# explicitly instead of using *
from .index import index_views
from .auth import auth_views
from .student import student_views
from .staff import staff_views


views = [index_views, auth_views, student_views, staff_views]

# blueprints must be added to this list
