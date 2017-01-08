def register_blueprint(app):
    from . import home
    from . import user
    app.register_blueprint(home.blueprint, url_prefix='')
    app.register_blueprint(user.blueprint, url_prefix='')
