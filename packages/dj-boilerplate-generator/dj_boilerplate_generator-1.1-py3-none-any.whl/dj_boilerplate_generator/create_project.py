import os
import sys


def create_app(project_name, app_name):
    if (bool(" " in app_name)
            or bool("-" in app_name)
            or app_name[0].isdigit()) is not True:
        os.system(f"cd {project_name} ;python3 manage.py startapp {app_name}")
        os.mkdir(f'{project_name}/{app_name}/templates')

        open(f"{project_name}/{app_name}/templates/index.html", 'a').close()
        print(
            f"Basic structure of {app_name} (django application) "
            "created successfully.")

    else:
        print("Invalid application name.Valid examples:[app_name, appname]")
        sys.exit(1)


def add_view(app_location, view_function):
    with open(app_location, "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        file_object.write(view_function)


def create_project():
    project_name = input('Enter project name:')
    if (bool(" " in project_name) or
            bool("-" in project_name) or
            project_name[0].isdigit()) is not True:
        project_exist = os.path.exists(project_name)

        if project_exist is not True:
            os.system(f"django-admin startproject {project_name}")
            print(f"Basic structure of {project_name} "
                  "(Django project) created successfully.")

            app_name = input("Enter application name:")
            create_app(project_name, app_name)

            settings_app_init = 'django.contrib.staticfiles\','
            dj_url_init = """urlpatterns = [
    path('admin/', admin.site.urls),
]"""
            settings_location = os.path.realpath(
                f"{project_name}/{project_name}/settings.py")

            urls_location = os.path.realpath(
                f"{project_name}/{project_name}/urls.py")

            open_settings = open(settings_location, "r")

            open_urls = open(urls_location, "r")

            read_settings = open_settings.read()

            read_urls = open_urls.read()

            if settings_app_init in read_settings:
                add_app = read_settings.replace(settings_app_init,
                                                settings_app_init +
                                                f'\n    \'{app_name}\''+',')

                with open(settings_location, 'w') as file:
                    file.write(add_app)

                if dj_url_init in read_urls:

                    with open(urls_location, 'w') as url_file:
                        add_url = read_urls.replace(
                            dj_url_init,
                            f"""from django.conf.urls import url\nfrom {app_name} import views\nurlpatterns = [\n    path('admin/', admin.site.urls),\n    url('index/', views.indexview)\n]""")
                        url_file.write(add_url)

                        app_location = os.path.realpath(
                            f"{project_name}/{app_name}/views.py")
                        add_view(
                            app_location, """def indexview(request):\n    return render(request, 'index.html')\n""")
        else:
            print("Failed to create project, "
                  f"{project_name} aleready exists!")
    else:
        print("Invalid project name."
              "Valid examples:[project_name,projectname]")


if __name__ == "__main__":
    # globals()[sys.argv[1]]()
    create_project()
