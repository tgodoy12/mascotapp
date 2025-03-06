from flask import Flask, jsonify
from dotenv import load_dotenv
from extensions import db
from flask_cors import CORS
import os
from src.models.User import User


load_dotenv()

def create_app():
    app = Flask(__name__)
  

    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")
    sslmode = "require"

    connection_string = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}?sslmode={sslmode}"

    app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        print("Verificando la conexión a la base de datos y modelos registrados...")

        try:
            print("\nModelos registrados en SQLAlchemy:")
            for clase in [User]:
                print(f"- {clase.__name__}: {clase.__tablename__}")

            inspector = db.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            print("\nTablas existentes en la base de datos:")
            for table in existing_tables:
                print(f"- {table}")

            if not existing_tables:
                print("\nNo se encontraron tablas. Procediendo a la creación...")
                db.create_all()
                db.session.commit()
                
                inspector = db.inspect(db.engine)
                created_tables = inspector.get_table_names()
                print("\nTablas creadas:")
                for table in created_tables:
                    print(f"- {table}")
                    columns = inspector.get_columns(table)
                    for column in columns:
                        print(f"  - {column['name']}: {column['type']}")
            else:
                print("\nTablas existentes:")
                for table in existing_tables:
                    print(f"- {table}")
                    columns = inspector.get_columns(table)
                    for column in columns:
                        print(f"  - {column['name']}: {column['type']}")
            
        except Exception as e:
            print(f"Error al verificar/crear las tablas: {str(e)}")
            db.session.rollback()
            raise

    @app.route("/api", methods=["GET"])
    def home():
        return jsonify({
            "message": "Backend connected",
            "result": "Successfully"
        })

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)

""" from flask import Flask
from src.extensions import db
from src.config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar la base de datos
db.init_app(app)

# Importar modelos después de inicializar db para evitar errores de importación
from src.models import user, mascota

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
 """