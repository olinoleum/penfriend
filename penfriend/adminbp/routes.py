# Third party imports
from flask_admin.contrib.sqla import ModelView
from flask import Blueprint
from flask_login import current_user

# Local application imports
from penfriend import admin, db
from penfriend.models import User, Message


adminblueprint = Blueprint('adminblueprint', __name__)


class MyModelView(ModelView):
    def is_accessible(self):
        return True


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Message, db.session))