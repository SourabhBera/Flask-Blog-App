from flask import Blueprint, render_template, url_for

errors = Blueprint('errors', __name__)



@errors.app_errorhandler(401)
def error_401(error):
    image_401 = url_for('static', filename='error_page/401.jpg')
    return render_template('error/401.html', image_401=image_401), 401


@errors.app_errorhandler(403)
def error_403(error):
    image_403 = url_for('static', filename='error_page/403.jpg')
    return render_template('error/403.html', image_403=image_403), 403


@errors.app_errorhandler(404)
def error_404(error):
    image_404 = url_for('static', filename='error_page/404.jpg')
    return render_template('error/404.html', image_404=image_404), 404


@errors.app_errorhandler(500)
def error_500(error):
    image_500 = url_for('static', filename='error_page/500.jpg')
    return render_template('error/500.html', image_500=image_500), 500

