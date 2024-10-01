import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, r2_score

# Carregando os dados
data = pd.read_csv("ChargeEvents_18_09.csv")

# Convertendo DurationTicks para horas
data['DurationHours'] = data['DurationTicks'] / 36000000000

# Criando dummies para ModeloCarro > converter a string para um valor númerico
car_model_dummies = pd.get_dummies(data['ModeloCarro'], prefix='ModeloCarro')
data = pd.concat([data, car_model_dummies], axis=1)

# Selecionando features e target
features = ['StartStateOfCharge'] + list(car_model_dummies.columns)
target = 'DurationHours'

# Separando os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(data[features], data[target], test_size=0.2, random_state=42)

# Criando um imputer para substituir NaN pela média da coluna
imputer = SimpleImputer(strategy='mean')

# Ajustando o imputer aos dados de treino e transformando treino e teste
X_train = imputer.fit_transform(X_train)
X_test = imputer.transform(X_test)

# Criando o modelo Random Forest
model = RandomForestRegressor(n_estimators=10000, random_state=42)

# Treinando o modelo
model.fit(X_train, y_train)

# Fazendo previsões com os dados de teste
y_pred = model.predict(X_test)

# Avaliando o modelo
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print('Mean Squared Error:', mse)
print('R-squared:', r2)

# Função para prever o tempo de recarga
def predict_charging_time(car_model, start_state_of_charge):
  # Criando um dataframe com as features
  features = pd.DataFrame({'StartStateOfCharge': [start_state_of_charge]})
  
  # Adicionando dummies para o modelo do carro
  for model_name in car_model_dummies.columns:
    features[model_name] = 0
  features['ModeloCarro_' + car_model] = 1
  
  # Fazendo a previsão
  duration_hours = model.predict(features)[0]
  
  return duration_hours

# Exemplo de uso da função
car_model = 'Kangoo Z.E. MAXI 2 Lugares 2P'
start_state_of_charge = 20

charging_time = predict_charging_time(car_model, start_state_of_charge)

print(f'Tempo de recarga previsto para {car_model} com {start_state_of_charge}% de carga inicial: {charging_time:.2f} horas')