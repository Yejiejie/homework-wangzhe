# -*- coding: utf-8 -*-
'''Python代码的主要含义是创造一个字典
        dict_all{'英雄名':[[被动技能,一技能,二技能,三技能],英雄故事]}'''
from flask import Flask, render_template, request, escape
import os

app = Flask(__name__)
os.getcwd()

dict_all = dict()
title = '欢迎来到王者荣耀'

file_names = [x.strip('.txt') for x in os.listdir('skill')]  #提取文件夹内所有文件名，即英雄名
for f in file_names:
    dict_all.setdefault(f)  #创建一个键为每个英雄名的字典，值为空
    dict_all[f] = list()
    with open('skill/{fn}'.format(fn=f+'.txt'),'r') as file_skill:
        dict_all[f].append(file_skill.read().splitlines())  #将英雄技能信息的列表添加到字典的值
        try:
            dict_all[f][0][0] = dict_all[f][0][0].strip('被动：')  #去掉列表里英雄被动技能前面的'被动：'，以便后面的网页输出
        except:
            pass
    try:
        with open('story/{fn}'.format(fn=f+'.txt'),'r') as file_story:
            dict_all[f].append(file_story.read())  #将英雄故事加入字典
    except FileNotFoundError:
        pass


'''以下部分作用是将Python代码和网页对接'''

@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    hero_name = request.form['input_hero_name']
    title = '以下是您的结果：'
    return render_template('results.html',
                           the_title=title,
                           the_name=hero_name,
                           output_skill_passive=dict_all['{fn}'.format(fn=hero_name)][0][0],
                           output_skill_1=dict_all['{fn}'.format(fn=hero_name)][0][1],
                           output_skill_2=dict_all['{fn}'.format(fn=hero_name)][0][2],
                           output_skill_3=dict_all['{fn}'.format(fn=hero_name)][0][3],
                           output_story=dict_all['{fn}'.format(fn=hero_name)][1]
                           )


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title=title)


if __name__ == '__main__':
    app.run(debug=True)
