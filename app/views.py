"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from flask import flash, render_template, request, redirect, send_from_directory, url_for
from unittest.mock import PropertyMock
from app import app, db
from app.forms import propertyForm
from werkzeug.utils import secure_filename
import os

from app.models import properties_info
###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Kabian Davidson")

@app.route('/properties/create', methods=['POST','GET'])
def property():
    form = propertyForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            photo = form.photo.data
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            title=form.title.data
            description=form.description.data
            bedroom=form.room.data
            bathroom=form.bathroom.data
            location=form.location.data
            price=form.price.data
            type=form.type.data
            db.session.add(properties_info(title,bedroom,bathroom,location,price,description,type,filename))
            db.session.commit()
            flash('Property Added Successfully!', 'success')
            return redirect(url_for('properties'))
    else:
        flash_errors(form)
    return render_template('new_property.html',form=form)

@app.route('/properties/<propertyid>')
def this_property(propertyid):
    property = properties_info.query.filter_by(id=propertyid).first()
    return render_template('property.html',property=property)

@app.route('/properties')
def properties():
    property = properties_info.query.all()
    return render_template('properties.html',property=property)

###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
