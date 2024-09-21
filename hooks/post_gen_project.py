"""
NOTE:
    the below code is to be maintained Python 2.x-compatible
    as the whole Cookiecutter Django project initialization
    can potentially be run in Python 2.x environment
    (at least so we presume in `pre_gen_project.py`).

TODO: restrict Cookiecutter Django project initialization to
      Python 3.x environments only
"""

from __future__ import print_function

import json
import os
import random
import shutil
import string

try:
    # Inspired by
    # https://github.com/django/django/blob/master/django/utils/crypto.py
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

DEBUG_VALUE = "debug"


def remove_open_source_files():
    file_names = ["CONTRIBUTORS.txt", "LICENSE"]
    for file_name in file_names:
        os.remove(file_name)


def remove_gplv3_files():
    file_names = ["COPYING"]
    for file_name in file_names:
        os.remove(file_name)


def remove_custom_user_manager_files():
    os.remove(
        os.path.join(
            "app",
            "{{cookiecutter.project_slug}}",
            "users",
            "managers.py",
        )
    )
    os.remove(
        os.path.join(
            "app",
            "{{cookiecutter.project_slug}}",
            "users",
            "tests",
            "test_managers.py",
        )
    )


def remove_pycharm_files():
    idea_dir_path = ".idea"
    if os.path.exists(idea_dir_path):
        shutil.rmtree(idea_dir_path)

    docs_dir_path = os.path.join("docs", "pycharm")
    if os.path.exists(docs_dir_path):
        shutil.rmtree(docs_dir_path)


def remove_utility_files():
    shutil.rmtree("utility")


def remove_sass_files():
    shutil.rmtree(os.path.join("app", "{{cookiecutter.project_slug}}", "static", "sass"))


def remove_gulp_files():
    file_names = ["gulpfile.js"]
    for file_name in file_names:
        os.remove(file_name)


def remove_webpack_files():
    shutil.rmtree("webpack")
    remove_vendors_js()


def remove_vendors_js():
    vendors_js_path = os.path.join(
        "{{ cookiecutter.project_slug }}",
        "static",
        "js",
        "vendors.js",
    )
    if os.path.exists(vendors_js_path):
        os.remove(vendors_js_path)


def remove_packagejson_file():
    file_names = ["package.json"]
    for file_name in file_names:
        os.remove(file_name)


def update_package_json(remove_dev_deps=None, remove_keys=None, scripts=None):
    remove_dev_deps = remove_dev_deps or []
    remove_keys = remove_keys or []
    scripts = scripts or {}
    with open("package.json", mode="r") as fd:
        content = json.load(fd)
    for package_name in remove_dev_deps:
        content["devDependencies"].pop(package_name)
    for key in remove_keys:
        content.pop(key)
    content["scripts"].update(scripts)
    with open("package.json", mode="w") as fd:
        json.dump(content, fd, ensure_ascii=False, indent=2)
        fd.write("\n")


def handle_js_runner(choice, use_async):
    if choice == "Gulp":
        update_package_json(
            remove_dev_deps=[
                "@babel/core",
                "@babel/preset-env",
                "babel-loader",
                "concurrently",
                "css-loader",
                "mini-css-extract-plugin",
                "postcss-loader",
                "postcss-preset-env",
                "sass-loader",
                "webpack",
                "webpack-bundle-tracker",
                "webpack-cli",
                "webpack-dev-server",
                "webpack-merge",
            ],
            remove_keys=["babel"],
            scripts={
                "dev": "gulp",
                "build": "gulp generate-assets",
            },
        )
        remove_webpack_files()
    elif choice == "Webpack":
        scripts = {
            "dev": "webpack serve --config webpack/dev.config.js",
            "build": "webpack --config webpack/prod.config.js",
        }
        remove_dev_deps = [
            "browser-sync",
            "cssnano",
            "gulp",
            "gulp-concat",
            "gulp-imagemin",
            "gulp-plumber",
            "gulp-postcss",
            "gulp-rename",
            "gulp-sass",
            "gulp-uglify-es",
        ]
        remove_dev_deps.append("concurrently")
        update_package_json(remove_dev_deps=remove_dev_deps, scripts=scripts)
        remove_gulp_files()


def remove_prettier_pre_commit():
    with open(".pre-commit-config.yaml", "r") as fd:
        content = fd.readlines()

    removing = False
    new_lines = []
    for line in content:
        if removing and "- repo:" in line:
            removing = False
        if "mirrors-prettier" in line:
            removing = True
        if not removing:
            new_lines.append(line)

    with open(".pre-commit-config.yaml", "w") as fd:
        fd.writelines(new_lines)


def remove_celery_files():
    file_names = [
        os.path.join("app", "config", "celery_app.py"),
        os.path.join("app", "{{ cookiecutter.project_slug }}", "users", "tasks.py"),
        os.path.join("app", "{{ cookiecutter.project_slug }}", "users", "tests", "test_tasks.py"),
    ]
    for file_name in file_names:
        os.remove(file_name)


def remove_async_files():
    file_names = [
        os.path.join("app", "config", "asgi.py"),
        os.path.join("app", "config", "websocket.py"),
    ]
    for file_name in file_names:
        os.remove(file_name)


def generate_random_string(length, using_digits=False, using_ascii_letters=False, using_punctuation=False):
    """
    Example:
        opting out for 50 symbol-long, [a-z][A-Z][0-9] string
        would yield log_2((26+26+50)^50) ~= 334 bit strength.
    """
    if not using_sysrandom:
        return None

    symbols = []
    if using_digits:
        symbols += string.digits
    if using_ascii_letters:
        symbols += string.ascii_letters
    if using_punctuation:
        all_punctuation = set(string.punctuation)
        # These symbols can cause issues in environment variables
        unsuitable = {"'", '"', "\\", "$"}
        suitable = all_punctuation.difference(unsuitable)
        symbols += "".join(suitable)
    return "".join([random.choice(symbols) for _ in range(length)])


def set_flag(file_path, flag, value=None, formatted=None, *args, **kwargs):
    if value is None:
        random_string = generate_random_string(*args, **kwargs)
        if random_string is None:
            print(
                "We couldn't find a secure pseudo-random number generator on your "
                "system. Please, make sure to manually {} later.".format(flag)
            )
            random_string = flag
        if formatted is not None:
            random_string = formatted.format(random_string)
        value = random_string

    with open(file_path, "r+") as f:
        file_contents = f.read().replace(flag, value)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    return value


def append_to_gitignore_file(ignored_line):
    with open(".gitignore", "a") as gitignore_file:
        gitignore_file.write(ignored_line)
        gitignore_file.write("\n")


def remove_celery_compose_dirs():
    shutil.rmtree(os.path.join("compose", "django", "celery"))


def remove_node_dockerfile():
    shutil.rmtree(os.path.join("compose", "node"))


def remove_drf_starter_files():
    os.remove(os.path.join("app", "config", "api_router.py"))
    shutil.rmtree(os.path.join("app", "{{cookiecutter.project_slug}}", "users", "api"))
    os.remove(os.path.join("app", "{{cookiecutter.project_slug}}", "users", "tests", "test_drf_urls.py"))
    os.remove(os.path.join("app", "{{cookiecutter.project_slug}}", "users", "tests", "test_drf_views.py"))
    os.remove(os.path.join("app", "{{cookiecutter.project_slug}}", "users", "tests", "test_swagger.py"))


def main():
    if "{{ cookiecutter.open_source_license }}" == "Not open source":
        remove_open_source_files()
    if "{{ cookiecutter.open_source_license}}" != "GPLv3":
        remove_gplv3_files()

    if "{{ cookiecutter.username_type }}" == "username":
        remove_custom_user_manager_files()

    if "{{ cookiecutter.editor }}" != "PyCharm":
        remove_pycharm_files()

    remove_utility_files()

    append_to_gitignore_file(".env")
    append_to_gitignore_file(".envs/*")

    if "{{ cookiecutter.frontend_pipeline }}" in ["None", "Django Compressor"]:
        remove_gulp_files()
        remove_webpack_files()
        remove_sass_files()
        remove_packagejson_file()
        remove_prettier_pre_commit()
        remove_node_dockerfile()
    else:
        handle_js_runner(
            "{{ cookiecutter.frontend_pipeline }}",
            use_async=("{{ cookiecutter.use_async }}".lower() == "y"),
        )

    if "{{ cookiecutter.use_celery }}".lower() == "n":
        remove_celery_files()
        remove_celery_compose_dirs()

    if "{{ cookiecutter.use_drf }}".lower() == "n":
        remove_drf_starter_files()

    if "{{ cookiecutter.use_async }}".lower() == "n":
        remove_async_files()

    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)


if __name__ == "__main__":
    main()
