import requests

search_api_url = 'http://127.0.0.1:7860/prediccion'
# search_api_url = 'https://qualliobootcamp.azurewebsites.net/prediccion'


# CASO 1 -> Tipo de fraude: 0/False
data = {
    "orderAmount" : 18.0,
    "orderState" : "pending",
    "paymentMethodRegistrationFailure" : "True",
    "paymentMethodType" : "card",
    "paymentMethodProvider" : "JCB 16 digit",
    "paymentMethodIssuer" : "Citizens First Banks",
    "transactionAmount" : 18,
    "transactionFailed" : False,
    "emailDomain" : "com",
    "emailProvider" : "yahoo",
    "customerIPAddressSimplified" : "only_numbers",
    "sameCity" : "yes"
}

# CASO 2 -> Tipo de fraude: 1/True
data_ = {
    "orderAmount" : 26.0,
    "orderState" : "fulfilled",
    "paymentMethodRegistrationFailure" : "True",
    "paymentMethodType" : "bitcoin",
    "paymentMethodProvider" : "VISA 16 digit",
    "paymentMethodIssuer" : "Solace Banks",
    "transactionAmount" : 26,
    "transactionFailed" : False,
    "emailDomain" : "com",
    "emailProvider" : "yahoo",
    "customerIPAddressSimplified" : "only_numbers",
    "sameCity" : "no"
}

response = requests.post(search_api_url, json=data)
print(response.status_code)
print(response.json())
