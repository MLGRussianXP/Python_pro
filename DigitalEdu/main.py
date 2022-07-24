import pandas as pd
import matplotlib.pyplot as plt


# очистка
# удаление ненужных элементов 
df = pd.read_csv('train.csv')
df.drop([
    'id', 'bdate', 'has_photo', 'has_mobile', 'followers_count', 'graduation', 'education_form', 'relation',
    'langs', 'people_main', 'city', 'last_seen', 'occupation_name'
], axis=1, inplace=True)


# главное в жизни
def life_main_apply(life_main):
    if life_main == '2':
        return 1
    return 0

df['life_main'] = df['life_main'].apply(life_main_apply)


# начало и конец карьеры
def career_start_end_apply(date):
    if date == 'False':
        return 0
    return 1


df['career_start'] = df['career_start'].apply(career_start_end_apply)
df['career_end'] = df['career_end'].apply(career_start_end_apply)


# статус обчуения
def status_apply(status):
    if status == "Undergraduate applicant":
        return 0
    elif status == "Student (Bachelor's)" or status == "Student (Master's)" or status == "Student (Specialist)":
        return 1
    elif status == "Alumnus (Bachelor's)" or status == "Alumnus (Master's)" or status == "Alumnus (Specialist)":
        return 2
    else:
        return 3


df['education_status'] = df['education_status'].apply(status_apply)


# текущее занятие пользователя
df['occupation_type'].fillna('university', inplace=True)


def occupation_type_apply(occupation_type):
    if occupation_type == 'university':
        return 1
    return 0


df['occupation_type'] = df['occupation_type'].apply(occupation_type_apply)

# пол
def sex_apply(sex):
    if sex == 2:
        return 0
    return 1


df['sex'] = df['sex'].apply(sex_apply)

###################
# Гипотезы
###################
# Пользователь скорее всего приобретёт курс, если...
# 1. Он сейчас нигде не работает.
# или
# 2. В его жизни главное "карьера и деньги" и он без образования
# или
# 3. Он мужчина и обучается в униврситете
###################

# Пользователь скорее всего приобретёт курс, если он сейчас нигде не работает.
print("1. Пользователь скорее всего приобретёт курс, если он сейчас нигде не работает.\n")
print("Да - так и есть.")

pd.Series(data=(df[df['career_start'] == 0][df['career_end'] == 0]['result'].value_counts()).head()).plot(kind='pie')
plt.show()
print("\n\n")

# Пользователь скорее всего приобретёт курс, если в его жизни главное "карьера и деньги" и он без образования.
print('2. Пользователь скорее всего приобретёт курс, если в его жизни главное "карьера и деньги" и он без образования.\n')
print("Нет. Показатели одинаковы")

pd.Series(data=(df[df['life_main'] == 1][df['education_status'] == 0]['result'].value_counts()).head()).plot(kind='pie')
plt.show()
print("\n\n")

# Пользователь скорее всего приобретёт курс, если он мужчина и обучается в униврситете.
print("3. Пользователь скорее всего приобретёт курс, если он мужчина и обучается в униврситете.\n")
print("Да.")

pd.Series(data=(df[df['sex'] == 1][df['occupation_type'] == 1]['result'].value_counts()).head()).plot(kind='pie')
plt.show()
print("\n\n")

# модель
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score

X = df.drop('result', axis=1)
sc = StandardScaler()
classifier = KNeighborsClassifier(n_neighbors=5)

y = df['result']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
print(y_test)
print(y_pred)
print('Процент правильно предсказанных исходов:', round(accuracy_score(y_test, y_pred) * 100, 2))
