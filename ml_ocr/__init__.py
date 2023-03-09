# from app import app
import os.path
import boto3
from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
from .models import ocr_detect, segmentation_ml, topic_modelling, analysis, summarizer, chronology
from .models.upload_data import get_db, ENV

app = Flask(__name__)
app.secret_key = 'super secret key'
db = get_db()
if ENV == "dev":
    UPLOAD_FOLDER = 'C:/Users/novneet.patnaik/Documents/GitHub/ML-Analysis-azure/ml_ocr/tmp/upload_files'
elif ENV == "qa":
    UPLOAD_FOLDER = '/ml_ocr/tmp/upload_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def create_app(test_config=None):
    return app


@app.route('/')
def index_login():
    return render_template('index.html')


@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/login.html')
def login():
    return render_template('login.html')


@app.route('/team.html')
def team():
    return render_template('team.html')


@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route('/services.html')
def services():
    return render_template('services.html')


@app.route('/blog.html')
def blog():
    return render_template('blog.html')


@app.route('/blog-details.html')
def blog_details():
    return render_template('blog-details.html')


@app.route('/contact.html')
def contact():
    return render_template('contact.html')


@app.route('/features.html', methods=["POST", "GET"])
def features():
    return render_template('features.html')


@app.route('/portfolio.html')
def portfolio():
    return render_template('portfolio.html')


@app.route('/portfolio-details.html')
def portfolio_details():
    return render_template('portfolio-details.html')


@app.route('/summarization.html')
def summarization():
    return render_template('summarization.html')


@app.route('/segmentation.html')
def segmentation():
    return render_template('segmentation.html')


@app.route('/segmentation_1.html')
def segmentation_1():
    return render_template('segmentation_1.html')


@app.route('/sentiment.html')
def sentiment():
    return render_template('sentiment.html')


@app.route('/sentiment_1.html')
def sentiment_1():
    return render_template('sentiment_1.html')


@app.route('/sentiment_all.html')
def sentiment_all():
    return render_template('sentiment_all.html')


@app.route('/topic.html')
def topic():
    return render_template('topic.html')


@app.route('/topic_1.html')
def topic_1():
    return render_template('topic_1.html')


@app.route('/topic_2.html')
def topic_2():
    return render_template('topic_2.html')


@app.route('/login_signup', methods=["POST", "GET"])
def login_signup():
    username = request.form.get("username")
    login_pword = request.form.get("login_password")
    if "confirm_password" in request.form.to_dict():
        security_answer = request.form.get("security_q")
        register_pw = request.form['confirm_password']
        mail_check = db.admin_creds.find({"username": username})
        if db.admin_creds.count_documents({"username": username}) == 0:
            db.admin_creds.insert_one({"email": username, "password": register_pw, "security_answer": security_answer})
            return render_template('upload.html')
        else:
            error = "Mail Used"
            flash('Mail already used, please try loging in')
            return redirect(url_for('index'))

    else:
        mail_check = db.admin_creds.find({"username": username})
        if db.admin_creds.count_documents({"username": username}) > 0:
            for i in mail_check:
                if i['password'] == login_pword:
                    return render_template('upload.html')
            error = "wrong password"
            flash('Username and Password do not match')
            return redirect(url_for('index'))
        else:
            error = "no such email"
            flash('Mail not found, please sign up')
            return redirect(url_for('index'))


@app.route('/forgot_password', methods=["POST", "GET"])
def forgot_password():
    return render_template('password_recovery.html')


@app.route('/upload.html', methods=['GET', 'POST'])
def upload_file():
    return render_template('upload.html')


@app.route('/select_pages', methods=['GET', 'POST'])
def select_pages():
    """
    This function accepts uploaded file requests and sends back the no of pages of the file
    :input: File/Files
    :return: no of pages of a file or of each file
    """
    file_list = request.files.getlist("file")
    filename_list = []
    counter = 0
    for f in file_list:
        if f.filename != "":
            if " " in f.filename:
                f.filename = f.filename.replace(" ", "_")
            filename_list.append(f.filename)

            # count the number of files
            counter = counter + 1

            # Get AWS Credentials from MongoDB
            data = db['creds'].find_one()
            s3_bucket = 'digimachine-mlocr'
            s3 = boto3.resource(
                service_name='s3',
                region_name='us-east-2',
                aws_access_key_id=data['aws_access_key_id'],
                aws_secret_access_key=data['aws_secret_access_key']
            )

            # Save file in the temporary folder
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_content = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb')
            s3.Bucket(s3_bucket).put_object(Key=filename, Body=file_content)

        else:
            error = "no file"
            flash('File Not Selected')
            return redirect(url_for('upload_file'))

        # Check extension and call the correct method
        # filename = filename["'file_list'"][0]
        split_tup = os.path.splitext(filename)
        file_extension = split_tup[1]

        """
        Extract Document Data using Textract and PyPDF2 Util
        Get all feature Data:
           1. Segmentation
           2. Summarization
           3. Topic Modelling
           4. Document Info
           5. Sentiment Analysis
        """

        pages = ocr_detect.count_pages(filename)
        pages_list = []
        # Send the no. of pages
        for i in range(pages):
            pages_list.append(i + 1)
        data = {"filename": filename, "pages": pages_list}
        return render_template("select_pages.html", output_data=data)


@app.route('/display_feature', methods=['GET', 'POST'])
def display_feature():
    """
    This function will take the desired feature that has been selected by the user and send the final analysis
    :input: filename,
    :return: json text
    """

    feature_list = request.args.to_dict(flat=False)
    feature_needed = feature_list["'Feature'"][0]
    filename = request.form.get("filename")
    page = request.form.get("page")
    if filename != "":
        if " " in filename:
            filename = filename.replace(" ", "_")

    # Check extension and call the correct method
    split_tup = os.path.splitext(filename)
    file_extension = split_tup[1]

    """
    Extract Document Data using Textract and PyPDF2 Util
    Get all feature Data:
       1. Segmentation
       2. Summarization
       3. Topic Modelling
       4. Document Info
       5. Sentiment Analysis
    """

    # Call the appropriate OCR function according to the extension
    output_data_1 = []
    if file_extension == ".png" or file_extension == ".jpg":
        pages = 1
    elif file_extension == ".pdf":
        output_data_1 = ocr_detect.get_pdf_extracted(filename, page)
        if output_data_1 == "No Data":
            raise Exception("No Data in File")
    elif file_extension == ".docx":
        output_data_1 = ocr_detect.get_docx_extracted(filename)
        if output_data_1 == "No Data":
            raise Exception("No Data in File")
    else:
        raise Exception("Wrong file type")

    # Send the OCR Data to required feature function and render template
    if feature_needed.strip("'\'") == "Summary":
        data = summarizer_func(output_data_1)
        # page_counter_list = []
        if page == "All":
            # for page_counter in range(len(output_data_1)):
            #     page_counter_list.append(page_counter)
            data['page'] = "All Pages"
        else:
            data['page'] = "Page "+str(page)
        counter = 0
        for page_data in data["summarization"]:
            counter = counter + 1
            page_data = "Page " +str(counter) + "    " + page_data
            data['summarization'][counter-1] = page_data
        return render_template('summarization.html', output_data=data)

    if feature_needed.strip("'\'") == "Segmentation":
        data = segmentation_func(output_data_1)
        return render_template('segmentation_1.html', output_data=data)


@app.route('/features', methods=['GET', 'POST'])
def all_features():
    filename = request.args.to_dict(flat=False)
    page_selection = request.form.get("page")
    data = {"filename": filename["'file_list'"][0], "page": page_selection}
    return render_template('features.html', output_data=data)


@app.route('/ocr_read', methods=['GET', 'POST'])
def textract_api():
    """//
    This end point accepts files or url names
    Sends the file for OCR Detection
      //"""

    if request.method == 'POST':
        filename = request.args.to_dict(flat=False)
        # Get file list
        # file_list = request.files.getlist("file")
        counter = 1
        sentiment_data = "Data Not Available"
        # for filename in file_list:

        # Check extension and call the correct method
        filename = filename["file"]
        split_tup = os.path.splitext(filename)
        file_extension = split_tup[1]

        # work on 1st file
        if counter == 1:
            filename_1 = filename
            if file_extension == ".png" or file_extension == ".jpg":
                output_data_1 = ocr_detect.detect_text(filename_1)
            elif file_extension == ".pdf":
                output_data_1, pages = ocr_detect.get_pdf_extracted(filename_1)
            elif file_extension == ".docx":
                output_data_1 = ocr_detect.get_docx_extracted(filename_1)
            else:
                raise Exception("Wrong file type")
            if output_data_1 == "No Data":
                raise Exception("No Data in File")


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    """//
    This end point accepts files or url names
    Sends the file for OCR Detection and Analysis
    Sends the url for conversion to pdf, then for OCR Detection and Analysis
      //"""

    if request.method == 'POST':
        # filename = request.args.to_dict(flat=False)
        # Get file list
        filename = request.files.get("file")
        filename = filename.filename
        counter = 1
        sentiment_data = "Data Not Available"
        segmentation_data = "Data Not Available"
        similarity_data = "Data Not Available"
        summarized_data = "Data Not Available"
        topic_modeling = "Data Not Available"
        analysis_text = "Data Not Available"
        pages = "Data Not Available"
        # for filename in file_list:

        # Check extension and call the correct method
        # filename = filename["file"]
        split_tup = os.path.splitext(filename)
        file_extension = split_tup[1]

        """
    Extract Document Data using Textract and PyPDF2 Util
    Get all feature Data:
       1. Segmentation
       2. Summarization
       3. Topic Modelling
       4. Document Info
       5. Sentiment Analysis
       """

        # work on 1st file
        if counter == 1:
            filename_1 = filename
            if file_extension == ".png" or file_extension == ".jpg":
                output_data_1 = ocr_detect.detect_text(filename_1)
            elif file_extension == ".pdf":
                output_data_1, pages = ocr_detect.get_pdf_extracted(filename_1)
            elif file_extension == ".docx":
                output_data_1 = ocr_detect.get_docx_extracted(filename_1)
            else:
                raise Exception("Wrong file type")
            if output_data_1 == "No Data":
                raise Exception("No Data in File")

            # Get Segmented Data
            result = ' '.join(output_data_1)
            segmentation_data = segmentation.segmentation_ml(result)

            # Get the sentiment analysis
            # Send the Segmented Data to calculate sentiment intensity
            sentiment_data = analysis.sentiment_analysis(segmentation_data)

            # chronological  data
            # chronology_data = chronology.chronology_ml(output_data_1)

            # LDA Modeling data
            topic_modeling, analysis_text = topic_modelling.process_docs(segmentation_data)

            # Analysis
            # analysis_dict = analysis_text

            # Summarization
            summarized_data = summarizer.summarization_ml(result)
            summarized_data = segmentation.segmentation_ml(summarized_data)

        # work on 2nd file
        elif counter == 2:
            filename_2 = filename
            if file_extension == ".png" or file_extension == ".jpg":
                output_data_2 = ocr_detect.detect_text(filename_2)
            elif file_extension == ".pdf":
                output_data_2, pages = ocr_detect.get_pdf_extracted(filename_2)
            elif file_extension == ".docx":
                output_data_2 = ocr_detect.get_docx_extracted(filename_2)
            else:
                raise Exception("Wrong file type")
            if output_data_2 == "No Data":
                raise Exception("No Data in File")

            # Get Segmentation Chunks
            result = ' '.join(output_data_2)
            segmentation_data = segmentation.segmentation_ml(result)

            # Get the sentiment analysis
            # Send the Segmented Data to calculate sentiment intensity
            sentiment_data = analysis.sentiment_analysis(segmentation_data)

            # chronological  data
            # chronology_data = chronology.chronology_ml(output_data_2)

            # LDA Modeling data
            topic_modeling, analysis_text = topic_modelling.process_docs(segmentation_data)

            # Summarization
            summarized_data = summarizer.summarization_ml(result)
            summarized_data = segmentation.segmentation_ml(summarized_data)

            similarity_data = "To calculate Similarity Index you need to upload more than one file."

        # output data for display
        data = {"sentiment_data": sentiment_data,
                "segmentation": segmentation_data,
                "similarity": similarity_data,
                "summarization": summarized_data,
                "topic_model": topic_modeling,
                "analysis": analysis_text,
                "pages": pages}

        # "decomposition": decomposition_data,
        # "chronology": chronology_data,
        # "topic": topic_modeling}
        return render_template('display.html', output_data=data)


def summarizer_func(output_data_1):
    """//
    This end point accepts files or url names
    Sends the file for OCR Detection and Analysis
    Sends the url for conversion to pdf, then for OCR Detection and Analysis
      //"""
    summarized_data_list = []
    # Get Segmented Data
    for page_wise in output_data_1:
        # Remove single word or length words
        print_list = [word for word in page_wise if ' ' in word]
        result = ' '.join(print_list)

        # Summarization
        summarized_data = summarizer.summarization_ml(result)
        summarized_data_list.append(summarized_data)

    # output data for display
    data = {"summarization": summarized_data_list}

    return data


def segmentation_func(output_data_1):
    """//
    This end point accepts files or url names
    Sends the file for OCR Detection and Analysis
    Sends the url for conversion to pdf, then for OCR Detection and Analysis
      //"""

    # Get Segmented Data
    result = ' '.join(output_data_1[0])
    segmented_data = segmentation_ml.segmentation_ml(result)

    # output data for display
    data = {"segmented_data": segmented_data}

    return data


def sentiment_analysis_func(output_data_1):
    """//
    This end point accepts files or url names
    Sends the file for OCR Detection and Analysis
    Sends the url for conversion to pdf, then for OCR Detection and Analysis
      //"""
    # Get Segmented Data
    result = ' '.join(output_data_1)
    segmentation_data = segmentation.segmentation_ml(result)

    # Get the sentiment analysis
    # Send the Segmented Data to calculate sentiment intensity
    sentiment_data = analysis.sentiment_analysis(segmentation_data)

    # output data for display
    data = {"sentiment_data": sentiment_data}

    return render_template('sentiment_analysis.html', output_data=data)


def topic_model_func(output_data_1):
    """//
    This end point accepts files or url names
    Sends the file for OCR Detection and Analysis
    Sends the url for conversion to pdf, then for OCR Detection and Analysis
      //"""
    # Get Segmented Data    `
    result = ' '.join(output_data_1)
    segmentation_data = segmentation.segmentation_ml(result)

    # LDA Modeling data
    topic_data, analysis_text = topic_modelling.process_docs(segmentation_data)

    # output data for display
    # topic_data_list = []
    # for i in topic_data:
    #     topic_data_list.append(i[1])
    # data = {"topic_data": "topic_data_list"}

    return render_template('topic_modelling.html', output_data=topic_data)


def chronology_func(output_data_1):
    """//
    This end point accepts files or url names
    Sends the file for OCR Detection and Analysis
    Sends the url for conversion to pdf, then for OCR Detection and Analysis
      //"""
    # Get Segmented Data
    result = ' '.join(output_data_1)
    chronological_data = chronology.chronology_ml(result)

    # output data for display
    data = {"chronology_data": chronological_data}

    return render_template('chronology.html', output_data=data)


@app.route('/api_scrapper', methods=['GET', 'POST'])
def scrapper_func():
    return render_template('api_scrapper.html')

