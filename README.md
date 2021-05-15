# DjangoEndTermProject - MiniAliexpress
What project has at this time:<br/>
2 applications: auth_, main <br/>
media - the directory for added images<br/>
utils - constants, validators<br/>
logs - files for logging actions<br/>
project settings - settings of the project<br/>

# settings:
installed apps - added rest_framework, rest_framework_jwt, 2 apps<br/>
my database - postgresql end-term<br/>
new AUTH_USER_MODEL - MainUser from auth_<br/>
rest_framework and logging settings<br/>

# Constants:
there are roles of users - client, staff, courier, superuser
# auth_:
Models:<br/>
MainUser - common model for Client, Staff, Courier<br/>
Profile for each client and courier<br/>
Card for each client<br/>
And MainUserManager<br/>
Serializers for each model<br/>
Views:<br/>
Views to register each user, authorization using jwt, updating Profile and Card<br/>
Urls for each View to access<br/>
There are custom permissions<br/>
Signals for card and profile on creating a user<br/>
# Main:
Models: <br/>
Category, Product - common model for Wear and Food, Order and Cart<br/>
Serializers for each model<br/>
Views to create, update, get, delete for each model depending on permissions<br/>
Urls for each view to access<br/>
Signals for Cart on creating a client or ordering<br/>

# Other stuff in the project
Class diagram of the project included<br/>
[class_diagram_django.pdf](https://github.com/WooWooNursat/DjangoEndTermProject/files/6483698/class_diagram_django.pdf)

Short description<br/>

