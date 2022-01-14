from flask import Flask, request, send_file, send_from_directory
from werkzeug import security  # 获取上传文件的文件名
import os
import datetime
from flask import render_template

# UPLOAD_FOLDER = r'D:\\code\\'
UPLOAD_FOLDER = r'.\\javaSQL\\'
ALLOW_EXTENSIONS = set(['txt', 'sql'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    if '.' in filename and filename.rsplit('.', 1)[1] in ALLOW_EXTENSIONS:
        return True
    else:
        return False


@app.route('/')
def index():
    return render_template('sql.html')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filenamePre = file.filename.split('.')[0]
            filenamesuf = file.filename.split('.')[1]
            tfilename = filenamePre + now + '.' + filenamesuf
            # tfilename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], tfilename))  # 保存文件
            # abslot = os.path.join(app.config['UPLOAD_FOLDER'] + tfilename)
            # print(abslot)
            # print(UPLOAD_FOLDER, tfilename)
            # codeway = request.form.get('code')
            # print(codeway)
            try:
                newFilenName = parse(UPLOAD_FOLDER, tfilename, 'GBK')
            except:
                # return render_template('codeError.html')
                try:
                    newFilenName = parse(UPLOAD_FOLDER, tfilename, 'UTF-8')
                except:
                    return render_template('codeError.html')
            # print(newFilenName)
            return render_template('sqlDownload.html', tfilename=newFilenName)  # 返回保存成功的信息


@app.route('/download/<ttfilename>')
def download(ttfilename):
    # print('1111')
    # ttdir = request.form['dir']
    # ttfilename = request.form['name']
    # print(ttfilename)
    dir = os.path.join(UPLOAD_FOLDER)
    print(dir)
    print(ttfilename)
    return send_from_directory(directory=dir, path=ttfilename, as_attachment=True)
    # return send_file(os.path.join (UPLOAD_FOLDER) + filename, as_attachment=True)


def parse(sql_path, sql_file, code_way):
    # now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    # sql_path = r'E:\\V3_CIM\\SQLFiles' + '\\'
    # sql_file = r'OnlineMsg.sql'
    # print(sql_path+sql_file)
    with open(sql_path + sql_file, "r", encoding=code_way) as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip('\n')
        newline = ' +" ' + line + ' "\n'
        # print(newline)
        newFileNamePre = sql_file.split('.')[0]
        newFileName = r'-{0}-javaSQL.sql'.format(newFileNamePre)
        newFile = r'{0}\\{1}'.format(sql_path, newFileName)
        with open(newFile, 'a', encoding=code_way) as f:
            f.write(newline)
    # print('complete')
    # print(newFileName)
    return newFileName


if __name__ == '__main__':
    app.run()
