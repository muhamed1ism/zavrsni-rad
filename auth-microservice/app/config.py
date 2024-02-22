from datetime import timedelta

# DATABASE
SQLALCHEMY_DATABASE_URI = 'sqlite:///auth.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT
JWT_SECRET_KEY = 'ef27ed2c021307e72ffd3a0a'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
