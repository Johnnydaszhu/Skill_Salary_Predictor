from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import pickle
app = Flask(__name__)

xgb_model_min_loaded = pickle.load(open('static/model/min_xgb.pickle', "rb"))
xgb_model_max_loaded = pickle.load(open('static/model/max_xgb.pickle', "rb"))



sel_features = ['rating', '.Net', 'AI', 'AWS', 'Azure', 'Big Data', 'Business Intelligence',
'C/C++', 'Cassandra', 'Data Analysis', 'Data Science', 'Data Warehouse', 'Excel',
'Git', 'HBase', 'Hadoop', 'Hive', 'Java', 'JavaScript', 'Kafka',
'Linux', 'MATLAB', 'Machine Learning', 'Microsoft Office',
'Microsoft SQL Server', 'MongoDB', 'MySQL', 'Natural Language Processing',
'NoSQL', 'Oracle', 'Perl', 'Pig', 'PostgreSQL', 'Project Management',
'Python', 'R', 'S3', 'SAS', 'SPSS', 'SQL', 'Scala', 'Scripting',
'Shell Scripting', 'Software Development', 'Spark', 'Tableau', 'TensorFlow']

# @app.route('/')
# def home():
#     return render_template('index.html')


@app.route('/')
def predict():
    rating = 3.6
    inputs_list = ['Tableau','Python','MySQL']

    # rating = request.form.get('rating')
    # inputs_list = request.form.getlist('skills_selected')
    print(inputs_list)

    def nyc_salary_with_skills(rating, inputs_list):
        sample_list = [0] * (len(sel_features))
        input_X = pd.DataFrame([sample_list],
                               columns=list(sel_features))

        for inputs in inputs_list:
            if inputs in list(input_X.columns):
                input_X[inputs] = 1
        input_X['rating'] = float(rating)
        salary = (int(xgb_model_min_loaded.predict(input_X)), int(xgb_model_max_loaded.predict(input_X)))
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
    Suggest_Skills = nyc_salary_with_skills_and(rating, inputs_list)['Suggest_Skills']
    Suggest_Skills_Skills = Suggest_Skills['Skill'].to_json(orient='records')
    Suggest_Skills_SkillsSalary = list(Suggest_Skills['Salary_Increase'])
    min_Suggest_Skills_SkillsSalary = list(Suggest_Skills['Salary_Increase'])[0]
    max_Suggest_Skills_SkillsSalary = round(list(Suggest_Skills['Salary_Increase'])[-1],0)

    skill_info = pd.read_csv('static/data/single_skill_info.csv',index_col=0).round(3)
    single_skill_info = skill_info[skill_info['name'].isin(inputs_list)]
    single_skill_info_names = list(single_skill_info['name'])
    single_skill_info_max = single_skill_info[['name','max']].to_dict('records')
    single_skill_info_avg = list(single_skill_info['avg'].values)
    single_skill_info_min = list(single_skill_info['min'].values)
    single_skill_info_max2 = list(single_skill_info['max'].values)
    single_skill_info_importance = list(single_skill_info['importance'].values)
    single_skill_info_avg_importance = np.array(single_skill_info[['avg','importance','name',]]).tolist()
    skill_info_avg_importance = np.array(skill_info[['avg','importance','name',]]).tolist()

    # dataforflask = pd.read_csv('static/data/2019-12-3NYC_df_noloc.csv')
    # data_average_min = dataforflask['min'].mean
    # data_average_max = dataforflask['max'].mean
    data_average_min = 58115
    data_average_max = 90512

    prediction_com = pd.read_csv('static/data/prediction_com.csv')
    y_min = np.array(prediction_com[['index','y_min']]).tolist()
    y_pred_min = np.array(prediction_com[['index','y_pred_min']]).tolist()
    y_max = np.array(prediction_com[['index','y_max']]).tolist()
    y_pred_max = np.array(prediction_com[['index','y_pred_max']]).tolist()

    hist_x = [14000., 16270., 18540., 20810., 23080., 25350., 27620.,
              29890., 32160., 34430., 36700., 38970., 41240., 43510.,
              45780., 48050., 50320., 52590., 54860., 57130., 59400.,
              61670., 63940., 66210., 68480., 70750., 73020., 75290.,
              77560., 79830., 82100., 84370., 86640., 88910., 91180.,
              93450., 95720., 97990., 100260., 102530., 104800., 107070.,
              109340., 111610., 113880., 116150., 118420., 120690., 122960.,
              125230., 127500., 129770., 132040., 134310., 136580., 138850.,
              141120., 143390., 145660., 147930., 150200., 152470., 154740.,
              157010., 159280., 161550., 163820., 166090., 168360., 170630.,
              172900., 175170., 177440., 179710., 181980., 184250., 186520.,
              188790., 191060., 193330., 195600., 197870., 200140., 202410.,
              204680., 206950., 209220., 211490., 213760., 216030., 218300.,
              220570., 222840., 225110., 227380., 229650., 231920., 234190.,
              236460., 238730., 241000.]
    hist_min = [  1.,   0.,   0.,   0.,   1.,   1.,   1.,   2.,   8.,  12.,  23.,
          50.,  35.,  50., 115.,  68.,  73.,  52.,  62.,  41.,  39.,  21.,
          31.,  26.,  12.,  20.,  19.,   8.,   3.,   9.,   8.,   3.,   7.,
           5.,   2.,   3.,   2.,   4.,   2.,   4.,   1.,   2.,   0.,   1.,
           3.,   1.,   0.,   2.,   0.,   0.,   1.,   2.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   1.,   1.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
           0.]
    hist_max = [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
          0.,  0.,  1.,  1.,  1., 11.,  4., 10., 11., 22., 16., 16., 44.,
         29., 28., 42., 45., 49., 44., 34., 41., 33., 34., 38., 37., 17.,
         10., 31., 18., 18., 16., 26.,  9.,  9.,  6.,  8.,  4., 11.,  5.,
          7.,  3.,  6.,  5.,  4.,  2.,  4.,  0.,  4.,  1.,  4.,  0.,  0.,
          1.,  2.,  0.,  0.,  2.,  2.,  1.,  0.,  2.,  1.,  2.,  0.,  1.,
          0.,  1.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,
          0.,  1.,  0.,  0.,  1.,  0.,  0.,  0.,  1.]


    return render_template('viz.html', Max_Salary=format(salary_max), Min_Salary=format(salary_min),Suggest_Skills=format(Suggest_Skills),
                           Suggest_Skills_Skills=format(Suggest_Skills_Skills),Suggest_Skills_SkillsSalary=format(Suggest_Skills_SkillsSalary),
                           max_Suggest_Skills_SkillsSalary=format(max_Suggest_Skills_SkillsSalary),min_Suggest_Skills_SkillsSalary=format(min_Suggest_Skills_SkillsSalary),
                           inputs_list=inputs_list,rating=format(rating),single_skill_info=single_skill_info, single_skill_info_max=format(single_skill_info_max),single_skill_info_max2=format(single_skill_info_max2),
                           single_skill_info_avg=format(single_skill_info_avg),single_skill_info_min=format(single_skill_info_min),single_skill_info_importance=format(single_skill_info_importance),
                           single_skill_info_avg_importance=format(single_skill_info_avg_importance),skill_info_avg_importance=format(skill_info_avg_importance),single_skill_info_names=format(single_skill_info_names),
                           data_average_min=format(data_average_min),data_average_max=format(data_average_max),
                           hist_x=hist_x,hist_min=hist_min,hist_max=hist_max,
                           y_pred_min=format(y_pred_min),y_min=format(y_min),y_max=format(y_max),y_pred_max=format(y_pred_max))


if __name__ == '__main__':
    app.run()
