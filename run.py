from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(host="localhost", port=6000, debug=True)
    # pip install -r requirements.txt
    # app.run(host="0.0.0.0", port=5000, debug=True)
