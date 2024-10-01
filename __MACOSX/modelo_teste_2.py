import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Lendo o arquivo CSV (substitua "ChargeEvents_18_09.csv" pelo nome do seu arquivo)
data = pd.read_csv("ChargeEvents_18_09.csv")

# Extraindo a coluna "ModeloCarro"
data["ModeloCarro"] = data["ModeloCarro"].str.split("|").str[0].str.strip()

# Selecionando as colunas relevantes
features = data[["ModeloCarro", "ChargeType", "EndStateOfCharge"]]
target = data["DurationTicks"]

# Codificando as features categóricas usando One-Hot Encoding
encoder = OneHotEncoder(handle_unknown='ignore')
encoded_features = encoder.fit_transform(features).toarray()

# Dividindo os dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(
    encoded_features, target, test_size=0.2, random_state=42
)

# Criando o modelo de Random Forest Regressor
model = RandomForestRegressor(random_state=42)

# Treinando o modelo com os dados de treinamento
model.fit(X_train, y_train)

# Fazendo previsões com os dados de teste
y_pred = model.predict(X_test)

# Calculando as métricas de erro
rmse = mean_squared_error(y_test, y_pred, squared=False)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse:.2f}")
print(f"MAE: {mae:.2f}")
print(f"R²: {r2:.2f}")





# ... (código para carregar o modelo treinado, como no exemplo anterior)

# Lista com todos os modelos de carros únicos
modelo_carros = ["Kangoo Z.E. MAXI", "E-Scudo", "E-Jumpy", "JAC iEV1200T", "Partner Rapid Business Pack", "E-Expert"]

# Criando o codificador One-Hot
encoder = OneHotEncoder(handle_unknown='ignore')
encoder.fit(pd.DataFrame(modelo_carros))



# ... (código para carregar o modelo treinado, como no exemplo anterior)

# Definindo os valores de entrada
modelo_carro = "Kangoo Z.E. MAXI"
charge_type = "AC"
end_state_of_charge = 61

# Codificando os valores de entrada
encoded_modelo_carro = encoder.transform(pd.DataFrame([modelo_carro])).toarray()
encoded_charge_type = encoder.transform(pd.DataFrame([charge_type])).toarray()
encoded_end_state_of_charge = [[end_state_of_charge]]

# Criando o array de entrada para o modelo
input_data = [
    *encoded_modelo_carro[0],
    *encoded_charge_type[0],
    *encoded_end_state_of_charge[0]
]

# Obter a predição
previsao_duracao = model.predict([input_data])

# Exibindo a predição
print(f"Predição da duração da recarga: {previsao_duracao[0]:.2f}")