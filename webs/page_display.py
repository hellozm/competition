from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from get_info import *
from train import load_dataset, train_1
from show_web_base_info import get_base_info


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'


class NameForm(FlaskForm):
    url = StringField('请输入评估网站地址：', validators=[DataRequired(), URL()])
    submit = SubmitField('确定')


@app.route('/', methods=['GET', 'POST'])
def display():
    url = None
    form = NameForm()
    reliability = ''
    info = ''
    info_flag = False
    error = ''
    if form.validate_on_submit():
        url = form.url.data
        s = Spider(url.split('//')[1].split(':')[0].split('/')[0])
        s.get_main_info()
        s.get_ip_location()
        s.get_qualification_info()
        s.get_site_loopholes_info()
        print(s.feature)
        info = get_base_info(url.split('//')[1].split(':')[0].split('/')[0])
        if isinstance(info, list):
            info_flag = True
        else:
            info_flag = False
        if len(s.feature) == 8:
            feature_list = s.feature
            data, target = load_dataset('feature_2.txt')
            reliability = train_1(data, target, feature_list)
        else:
            error = '特征缺失，无法评估。'
    return render_template('display.html',
                           form=form,
                           url=url,
                           reliability=reliability,
                           info=info,
                           info_flag=info_flag,
                           error=error)


if __name__ == '__main__':
    app.run(debug=True)
