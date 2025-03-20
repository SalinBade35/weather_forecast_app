# yo app lai chahiney jati sabai urls yetai rakhne

from django.urls import path
# from .views import home, form, contact, about
from .views import * # * means all 



urlpatterns = [
    path("", home, name="home"),
    path("form/", form, name="form"),
    path("contact/", contact, name="contact"),
    path("about/", about, name="about"),
    path("delete/<int:id>", delete_data, name='delete_data'),
    path("recycle/", recycle, name="recycle"),
    path("restore/<int:id>", restore, name="restore"),
    path("clear_items/", clear_items, name="clear_items"),
    path("restore_all/", restore_all, name="restore_all"),
    path("edit/<int:id>", edit, name="edit"),
    

]


