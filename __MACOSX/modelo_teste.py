import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Lendo o arquivo CSV
data = pd.read_csv("ChargeEvents_18_09.csv")

# Extraindo a coluna "ModeloCarro"
data["ModeloCarro"] = data["ModeloCarro"].str.split("|").str[0].str.strip()

# Selecionando as colunas relevantes
features = data[["ModeloCarro", "ChargeType"]]
target = data["DurationTicks"]

# Codificando as features categóricas usando One-Hot Encoding
encoder = OneHotEncoder(handle_unknown='ignore')
encoded_features = encoder.fit_transform(features).toarray()

# Dividindo os dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(
    encoded_features, target, test_size=0.2, random_state=42
)

# Criando o modelo de regressão linear
model = LinearRegression()

# Treinando o modelo com os dados de treinamento
model.fit(X_train, y_train)

# Fazendo previsões com os dados de teste
y_pred = model.predict(X_test)

# Calculando as métricas de erro
rmse = mean_squared_error(y_test, y_pred, squared=False)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(X_test)
print(f"RMSE: {rmse:.2f}")
print(f"MAE: {mae:.2f}")
print(f"R²: {r2:.2f}")

