"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import render_template
from application import app
from application import views

app.add_url_rule('/', view_func=views.index, methods=['GET','POST'])
app.add_url_rule('/search', view_func=views.search,methods=['GET','POST'])
app.add_url_rule('/skratenici', view_func=views.skratenici,methods=['GET'])
app.add_url_rule('/predgovor', view_func=views.predgovor,methods=['GET'])

## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

