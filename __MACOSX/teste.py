import pickle
import pandas as pd

# Carregue o modelo treinado
model = pickle.load(open('charge_time_model.pkl', 'rb'))

# Crie novos dados de entrada
new_data = pd.DataFrame({'DurationTicks': [8934752043750]})

# Faça previsões com os novos dados
prediction = model.predict(new_data)

# Imprima a previsão
print('Previsão do tempo de recarga:', prediction[0])