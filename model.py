import pickle
import pandas as pd
import numpy as np
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField

xgb_model_min_loaded = pickle.load(open('static/ny_min_xgb_model_min.pickle', "rb"))
xgb_model_max_loaded = pickle.load(open('static/ny_max_xgb_model_min.pickle', "rb"))

sel_features = ['rating', 'AI', 'AWS', 'Azure', 'Big-Data', 'C/C++', 'Data-Analysis',
                'Data-Warehouse', 'Hadoop', 'Hive', 'Java', 'Kafka', 'Linux', 'MATLAB',
                'Machine-Learning', 'Microsoft-Office', 'Microsoft-SQL-Server',
                'Natural-Language-Processing', 'NoSQL', 'Oracle', 'Pig', 'Python', 'R',
                'SAS', 'SQL', 'Scala', 'Scripting', 'Spark', 'Tableau', 'TensorFlow']


class Get_Salary():

    def NYC_salary_with_skills(rating, inputs_list):
        sample_list = [0] * (len(sel_features))
        input_X = pd.DataFrame([sample_list],
                               columns=list(sel_features))

        for inputs in inputs_list:
            if inputs in list(input_X.columns):
                input_X[inputs] = 1
        input_X['rating'] = rating
        salary = (int(xgb_model_min_loaded.predict(input_X[:1])), int(xgb_model_max_loaded.predict(input_X[:1])))
        return salary

    skill_money = {}
    skill_money_list = []
    for skill in sel_features[1:]:
        skill_money['skill'] = skill
        skill_money['salary'] = NYC_salary_with_skills(3.6, [skill])
        skill_money_list.append(skill_money)
        skill_money = {}
    single_skill = pd.DataFrame(skill_money_list).sort_values('salary', ascending=False)

    def NYC_salary_with_skills_and(rating, inputs_list):
        sample_list = [0] * (len(sel_features))
        input_X = pd.DataFrame([sample_list],
                               columns=list(sel_features))

        for inputs in inputs_list:
            if inputs in list(input_X.columns):
                input_X[inputs] = 1
        salary = (int(xgb_model_min_loaded.predict(input_X[:1])), int(xgb_model_max_loaded.predict(input_X[:1])))

        # suggest skill with more salary
        suggest_list = []
        all_list = inputs_list

        for skill in single_skill['skill'][:10]:
            if skill not in inputs_list:
                suggest_list.append(skill)

            suggest_list_salary = {}
            suggest_list_salary_list = []
            for skill in suggest_list:
                all_list = []
                all_list = inputs_list + [skill]
                suggest_list_salary['skill'] = skill
                suggest_list_salary['salary'] = int(np.subtract(NYC_salary_with_skills(rating, all_list),
                                                                NYC_salary_with_skills(rating, inputs_list)).mean())
                suggest_list_salary_list.append(suggest_list_salary)
                suggest_list_salary = {}
        suggest_skills = pd.DataFrame(suggest_list_salary_list).sort_values('salary', ascending=False)
        suggest_skills = suggest_skills[suggest_skills['salary'] > 0]
        suggest_skills.columns = ['Skill', 'Salary increase by $']
        suggest_skills
        print('Annual Salary Range($):', salary)
        return suggest_skills[:3]

return NYC_salary_with_skills_and(3.6, ['Python,Tableau,AWS']):