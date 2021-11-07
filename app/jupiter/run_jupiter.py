# A script that's needed to setup django if it's not already running on a server.
# Without this, you won't be able to import django modules
# %%
import sys
import os
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PWD = r'c:\Users\Krzyz\OneDrive\Desktop\project_amber\app'
sys.path.append(PWD)
print(sys.path)


def init_django(project_name=None):
    # Find the project base directory

    # Add the project base directory to the sys.path
    # This means the script will look in the base directory for any module imports
    # Therefore you'll be able to import analysis.models etc
    sys.path.insert(0, BASE_DIR)

    # The DJANGO_SETTINGS_MODULE has to be set to allow us to access django imports
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{project_name}.settings")

    #  Allow queryset filtering asynchronously when running in a Jupyter notebook
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    # This is for setting up django
    django.setup()

# %%
# import sys
# PWD = r'c:\Users\Krzyz\OneDrive\Desktop\project_amber\app'
# sys.path.append(PWD)
# print(sys.path)
# from jupiter.run_jupiter import init_django
# init_django('app')
