from django.contrib.auth.models import User



def create_user(requester, **data):
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")   

    
    user = User.objects.create_user(
    email=email,
    username=username,
    password=password
    )

    user.username="saad"
    user.save
    return user






def change_password(requester, **data):

    password = data.get("password")   
    requester.set_password(password)
    requester.save()
    

    
    return requester