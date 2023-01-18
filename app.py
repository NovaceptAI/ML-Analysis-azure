import ml_ocr.__init__
app = ml_ocr.create_app()
# app.config['GOOGLE_APPLICATION_CREDENTIALS'] = "./panrange-online-b1dbaad59f70.json"
app.secret_key = 'super secret key'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
