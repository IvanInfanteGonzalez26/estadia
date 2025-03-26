class Config:
    
    #Configuración de base dedatos 
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1234@localhost:3306/blog_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "mi-super-secreto"
