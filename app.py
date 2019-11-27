from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import pickle
app = Flask(__name__)

xgb_model_min_loaded = pickle.load(open('static/model/ny_min_xgb_NOV_18.pickle', "rb"))
xgb_model_max_loaded = pickle.load(open('static/model/ny_max_xgb_NOV_18.pickle', "rb"))



sel_features = ['rating','.Net', 'AI', 'AWS', 'Azure', 'Big Data', 'Business Intelligence',
                'C/C++', 'Data Analysis', 'Data Science', 'Data Warehouse', 'Excel',
                'Git', 'HBase', 'Hadoop', 'Hive', 'Java', 'JavaScript', 'Kafka',
                'Linux', 'MATLAB', 'Machine Learning', 'Microsoft Office',
                'Microsoft SQL Server', 'MongoDB', 'MySQL', 'Natural Language Processing',
                'NoSQL', 'Oracle', 'Perl', 'Pig', 'PostgreSQL', 'Project Management',
                'Python', 'R', 'S3', 'SAS', 'SPSS', 'SQL', 'Scala', 'Scripting',
                'Shell Scripting', 'Software Development', 'Spark', 'Tableau', 'TensorFlow']

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST','GET'])
def predict():
    rating = request.form.get('rating')
    inputs_list = request.form.getlist('skills_selected')
    print(inputs_list)

    def nyc_salary_with_skills(rating, inputs_list):
        sample_list = [0] * (len(sel_features))
        input_X = pd.DataFrame([sample_list],
                               columns=list(sel_features))

        for inputs in inputs_list:
            if inputs in list(input_X.columns):
                input_X[inputs] = 1
        input_X['rating'] = float(rating)
        salary = (int(xgb_model_min_loaded.predict(input_X[:1])), int(xgb_model_max_loaded.predict(input_X[:1])))
        return salary

    skill_money = {}
    skill_money_list = []
    for skill in sel_features[1:]:
        skill_money['skill'] = skill
        skill_money['salary'] = nyc_salary_with_skills(3.6, [skill])
        skill_money_list.append(skill_money)
        skill_money = {}
    single_skill = pd.DataFrame(skill_money_list).sort_values('salary', ascending=False)

    def nyc_salary_with_skills_and(rating, inputs_list):

        sample_list = [0] * (len(sel_features))
        input_x = pd.DataFrame([sample_list],
                               columns=list(sel_features))

        for inputs in inputs_list:
            if inputs in list(input_x.columns):
                input_x[inputs] = 1
        input_x['rating'] = float(rating)
        salary_min = int(xgb_model_min_loaded.predict(input_x))
        salary_max = int(xgb_model_max_loaded.predict(input_x))

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
                suggest_list_salary['salary'] = int(np.subtract(nyc_salary_with_skills(rating, all_list),
                                                                nyc_salary_with_skills(rating, inputs_list)).mean())
                suggest_list_salary_list.append(suggest_list_salary)
                suggest_list_salary = {}
        suggest_skills = pd.DataFrame(suggest_list_salary_list).sort_values('salary', ascending=True)
        suggest_skills = suggest_skills[suggest_skills['salary'] > 0]
        suggest_skills.columns = ['Skill', 'Salary_Increase']
        return {'Min_Salary': salary_min, 'Max_Salary': salary_max, 'Suggest_Skills': suggest_skills}

    salary_min = int(nyc_salary_with_skills_and(rating, inputs_list)['Min_Salary'])
    salary_max = int(nyc_salary_with_skills_and(rating, inputs_list)['Max_Salary'])
    Suggest_Skills = nyc_salary_with_skills_and(rating, inputs_list)['Suggest_Skills'][:3]
    Suggest_Skills_Skills = Suggest_Skills['Skill'].to_json(orient='records')
    Suggest_Skills_SkillsSalary = list(Suggest_Skills['Salary_Increase'])
    max_Suggest_Skills_SkillsSalary = list(Suggest_Skills['Salary_Increase'])[0]
    min_Suggest_Skills_SkillsSalary = list(Suggest_Skills['Salary_Increase'])[-1]

    skill_info = pd.read_csv('static/data/single_skill_info.csv',index_col=0)
    single_skill_info = skill_info[skill_info['name'].isin(inputs_list)]
    single_skill_info_max = single_skill_info[['name','Max']].to_dict('records')
    single_skill_info_avg = list(single_skill_info['Avg'].values)
    single_skill_info_min = list(single_skill_info['Min'].values)




    return render_template('index.html', Max_Salary=format(salary_max), Min_Salary=format(salary_min),Suggest_Skills=format(Suggest_Skills),
                           Suggest_Skills_Skills=format(Suggest_Skills_Skills),Suggest_Skills_SkillsSalary=format(Suggest_Skills_SkillsSalary),
                           max_Suggest_Skills_SkillsSalary=format(max_Suggest_Skills_SkillsSalary),min_Suggest_Skills_SkillsSalary=format(min_Suggest_Skills_SkillsSalary),
                           inputs_list=inputs_list,rating=format(rating),single_skill_info=single_skill_info, single_skill_info_max=format(single_skill_info_max),
                           single_skill_info_avg=format(single_skill_info_avg),single_skill_info_min=format(single_skill_info_min))


if __name__ == '__main__':
    app.run(debug=True)
