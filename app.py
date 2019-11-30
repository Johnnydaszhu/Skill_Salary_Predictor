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


@app.route('/viz', methods=['POST','GET'])
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
    Suggest_Skills = nyc_salary_with_skills_and(rating, inputs_list)['Suggest_Skills'][:6]
    Suggest_Skills_Skills = Suggest_Skills['Skill'].to_json(orient='records')
    Suggest_Skills_SkillsSalary = list(Suggest_Skills['Salary_Increase'])
    max_Suggest_Skills_SkillsSalary = list(Suggest_Skills['Salary_Increase'])[0]
    min_Suggest_Skills_SkillsSalary = list(Suggest_Skills['Salary_Increase'])[-1]

    skill_info = pd.read_csv('static/data/single_skill_info.csv',index_col=0)
    single_skill_info = skill_info[skill_info['name'].isin(inputs_list)]
    single_skill_info_names = list(single_skill_info['name'])
    single_skill_info_max = single_skill_info[['name','max']].to_dict('records')
    single_skill_info_avg = list(single_skill_info['avg'].values)
    single_skill_info_min = list(single_skill_info['min'].values)
    single_skill_info_max2 = list(single_skill_info['max'].values)
    single_skill_info_ratio = list(single_skill_info['Ratio'].values)
    single_skill_info_avg_ratio = np.array(single_skill_info[['avg','Ratio','name',]]).tolist()
    skill_info_avg_ratio = np.array(skill_info[['avg','Ratio','name',]]).tolist()

    data_average_min = 57498
    data_average_max = 91356

    hist_x = [ 30000,  33860,  37720,  41580,  45440,  49300,  53160,
                     57020,  60880,  64740,  68600,  72460,  76320,  80180,
                     84040,  87900,  91760,  95620,  99480, 103340, 107200,
                    111060, 114920, 118780, 122640, 126500, 130360, 134220,
                    138080, 141940, 145800, 149660, 153520, 157380, 161240,
                    165100, 168960, 172820, 176680, 180540, 184400, 188260,
                    192120, 195980, 199840, 203700, 207560, 211420, 215280,
                    219140, 223000]
    hist_min = [ 3, 17, 41, 46, 72, 78, 49, 36, 28, 28, 14, 21,  5,
                      9,  6,  6,  5,  4,  3,  2,  3,  0,  3,  2,  0,  1,
                      2,  0,  0,  0,  0,  0,  1,  1,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
    hist_max = [ 0,  0,  0,  0,  0,  2, 11,  8, 18, 28, 31, 38, 51,
                     42, 40, 26, 35, 26, 16, 18, 15,  9, 16, 12,  5,  4,
                      7,  3,  1,  3,  2,  3,  3,  0,  1,  0,  2,  1,  2,
                      1,  2,  1,  1,  0,  0,  0,  1,  0,  0,  1]



    return render_template('viz.html', Max_Salary=format(salary_max), Min_Salary=format(salary_min),Suggest_Skills=format(Suggest_Skills),
                           Suggest_Skills_Skills=format(Suggest_Skills_Skills),Suggest_Skills_SkillsSalary=format(Suggest_Skills_SkillsSalary),
                           max_Suggest_Skills_SkillsSalary=format(max_Suggest_Skills_SkillsSalary),min_Suggest_Skills_SkillsSalary=format(min_Suggest_Skills_SkillsSalary),
                           inputs_list=inputs_list,rating=format(rating),single_skill_info=single_skill_info, single_skill_info_max=format(single_skill_info_max),single_skill_info_max2=format(single_skill_info_max2),
                           single_skill_info_avg=format(single_skill_info_avg),single_skill_info_min=format(single_skill_info_min),single_skill_info_ratio=format(single_skill_info_ratio),
                           single_skill_info_avg_ratio=format(single_skill_info_avg_ratio),skill_info_avg_ratio=format(skill_info_avg_ratio),single_skill_info_names=format(single_skill_info_names),
                           data_average_min=format(data_average_min),data_average_max=format(data_average_max),
                           hist_x=hist_x,hist_min=hist_min,hist_max=hist_max)


if __name__ == '__main__':
    app.run(debug=True)
