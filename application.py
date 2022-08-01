import os
import api

from app import app, login_manager
from models.models import User


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


app.config["Upload_folder"] = "./utils"
_ = api
app.run(host="0.0.0.0", port=os.environ.get("PORT", 5001))
