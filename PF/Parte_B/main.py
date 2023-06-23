from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

import pickle
import pandas as pd
from fastapi.encoders import jsonable_encoder


app = FastAPI()

MODEL_PATH = "data/modelo_proyecto_final.pkl"
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

COLUMNS_PATH = "data/categories_ohe_without_fraudulent.pickle"
with open(COLUMNS_PATH, "rb") as handle:
    ohe_tr = pickle.load(handle)

BINS_ORDER = "data/saved_bins_order.pickle"
with open(BINS_ORDER, 'rb') as handle:
    new_saved_bins_order = pickle.load(handle)

BINS_TRANSACTION = "data/saved_bins_transaction.pickle"
with open(BINS_TRANSACTION, 'rb') as handle:
    new_saved_bins_transaction = pickle.load(handle)


class Answer(BaseModel):
    orderAmount : float
    orderState : str
    paymentMethodRegistrationFailure : str
    paymentMethodType : str
    paymentMethodProvider : str
    paymentMethodIssuer : str
    transactionAmount : float
    transactionFailed : bool
    emailDomain : str
    emailProvider : str
    customerIPAddressSimplified : str
    sameCity : str


@app.get("/")
async def root():
    return {"message": "Proyecto Final Bootcamp de EDVAI"}


@app.post("/prediccion")
def predict_fraud_customer(answer: Answer):

    answer_dict = jsonable_encoder(answer)
    
    for key, value in answer_dict.items():
        answer_dict[key] = [value]

    # Crear dataframe
    single_instance = pd.DataFrame.from_dict(answer_dict)

    # Manejar puntos de corte o bins
    single_instance["orderAmount"] = single_instance["orderAmount"].astype(float)
    single_instance["orderAmount"] = pd.cut(single_instance['orderAmount'],
                                    bins=new_saved_bins_order, 
                                    include_lowest=True)

    single_instance["transactionAmount"] = single_instance["transactionAmount"].astype(int)
    single_instance["transactionAmount"] = pd.cut(single_instance['transactionAmount'],
                                    bins=new_saved_bins_order, 
                                    include_lowest=True)

    # One hot encoding
    single_instance_ohe = pd.get_dummies(single_instance).reindex(columns = ohe_tr).fillna(0)
    prediction = model.predict(single_instance_ohe)

    # Cast numpy.int64 to just a int
    type_of_fraud = int(prediction[0])
    response = {"Tipo de fraude": type_of_fraud}
    
    return response



if __name__ == '__main__':

    uvicorn.run(app, host='0.0.0.0', port=7860)
