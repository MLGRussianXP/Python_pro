import pandas as pd
import matplotlib.pyplot as plt

cols = list(pd.read_csv("Space_Corrected.csv", nrows=1))
df = pd.read_csv("Space_Corrected.csv", usecols=[i for i in cols if i != 'Unnamed: 0'])


# 1. При статусе миссии "Status Mission", отличного от "Success", 
# стоимость миссии "Rocket" чаще всего не указана.
print('1. При статусе миссии "Status Mission", отличного от "Success", стоимость миссии "Rocket" чаще всего не указана.\n')
print("\nВидно, что незаполненных ячеек стоимости миссии намного больше, чем заполненных.\n" +
"Гипотеза 1 подтверждена.\n\n")

pd.Series(data=pd.isnull(df[df['Status Mission'] != "Success"]['Rocket']).value_counts()).plot(kind='bar')
plt.show()


# 2. Страна, с которой чаще всего отправляют ракеты - "USA".
print('2. Страна, с которой чаще всего отправляют ракеты - "USA"\n')
print(
    "Как мы видим, наибольшее число ракет отправляют с России, тем не менее США отстаёт от неё буквально на 20-30 запусков."
    f"\nГипотеза 2 опровергнута.\n\n"
)

def to_country(place):
    return str(place).split(", ")[-1]

pd.Series(data=df['Location'].apply(to_country).value_counts()).plot(kind='barh')
plt.show()


# 3. Миссии компании "Company Name" "SpaceX" самые успешные среди всех остальных.
print('3. Миссии компании "Company Name" "SpaceX" самые успешные среди всех остальных.\n')
print(
    "Не только SpaceX имеет самые успешные показатели.\n"
    "Помимо неё есть ещё 3 компании: VKS RF, i-Space и Virgin Orbit.\n"
    "Гипотеза 3 опровергнута."
)

pd.Series(data=df.groupby(by="Status Mission")["Company Name"].max().value_counts()).plot(kind='barh')
plt.show()
