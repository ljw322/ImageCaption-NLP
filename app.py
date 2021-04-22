from flask import Flask, render_template, redirect, request, flash
from apscheduler.schedulers.background import BackgroundScheduler
import time
import atexit
import Caption_it
import Category_it
import Crawling_it


scheduler = BackgroundScheduler()
# scheduler.add_job(func=Crawling_it.run, trigger="interval", seconds=60)
scheduler.add_job(Crawling_it.run, 'cron', day_of_week='mon')
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

# __name == __main__
app = Flask(__name__)
app.config["SECRET_KEY"] = "ABCD"

ImagePath = ''
Sen = ''

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/caption', methods=['POST'])
def marks():
    if request.method == "POST":
        global ImagePath
        global Sen
        error = None
        result_dic = {}
    
        f = request.files['userfile']

        if not f.filename :
            error = 'Please upload your image!'
        else:
            ImagePath = "./static/image/{}".format(f.filename) #./static/images.jpg
            f.save(ImagePath)
            Sen = Caption_it.caption_this_image(ImagePath)

            result_dic = {
                'image':ImagePath,
                'caption':Sen
            }
        # print(caption)
    
    return render_template("index.html", result_dic = result_dic, error=error)

@app.route('/category', methods=['POST'])
def result():
    if request.method == "POST":

        # sen = request.form['sentence']

        # image_data = request.form.get("uploadImage")
        # f = request.files['userfile']
        # path = "./static/{}".format(f.filename) #./static/images.jpg
        # print("imageData:", image_data)

        result_dic = {
            'image':ImagePath,
            'caption':Sen
        }        

        category, tempTagList = Category_it.recommendTags(Sen)
        print("category is:", category, "tempTagList:", tempTagList)
    
    return render_template("index.html",  result_dic = result_dic, result_category = category, result_tags = tempTagList)


if __name__ == '__main__':
    app.run(debug = True)