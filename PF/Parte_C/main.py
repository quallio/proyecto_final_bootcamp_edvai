from fastapi import FastAPI
import gradio as gr
import pickle
import pandas as pd

# esto se ejecuta directamente ejecutando con python este file ...

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


PARAMS_NAME = [
    "orderAmount",
    "orderState",
    "paymentMethodRegistrationFailure",
    "paymentMethodType",
    "paymentMethodProvider",
    "paymentMethodIssuer",
    "transactionAmount",
    "transactionFailed",
    "emailDomain",
    "emailProvider",
    "customerIPAddressSimplified",
    "sameCity",
]


def predict_fraud_customer(*args):

    answer_dict = {}

    for i in range(len(PARAMS_NAME)):
        answer_dict[PARAMS_NAME[i]] = [args[i]]


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
    # Adaptación respuesta
    response = "Error parsing value"
    if type_of_fraud == 0:
        response = "False"
    if type_of_fraud == 1:
        response = "True"
    if type_of_fraud == 2:
        response = "Warning"
        
    return response


with gr.Blocks() as demo:
    gr.Markdown(
        """
        # Fraude o no fraude ??
        """
    )

    with gr.Row():
        with gr.Column():

            gr.Markdown(
                """
                ## Averiguar si la compra es fraudulenta o no
                """
            )

            orderAmount = gr.Slider(label="Order amount", minimum=0, maximum=355, step=1, randomize=True)
            
            orderState = gr.Radio(
                label="Order state",
                choices=["failed", "fulfilled", "pending"],
                value="failed"
                )
            
            paymentMethodRegistrationFailure = gr.Radio(
                label="Payment method registration failure",
                choices=["True", "False"],
                value="True"
                )
            
            paymentMethodType = gr.Radio(
                label="Payment method type",
                choices=["apple pay", "bitcoin", "card", "paypal"],
                value="card"
                )

            paymentMethodProvider = gr.Dropdown(
                label="Payment method provider",
                choices=["American Express", "Discover", "Maestro", "Diners Club / Carte Blanche", "Mastercard", "Voyager", "JCB", "VISA"],
                multiselect=False,
                value="Amereican Express"
                )

            paymentMethodIssuer = gr.Dropdown(
                label="Payment method issuer",
                choices=["weird", "Citizens First Banks", "Rose Bancshares", "Grand Credit Corporation", "Solace Banks",  "Bastion Banks", "Bulwark Trust Corp.", "Her Majesty Trust", "Vertex Bancorp", "Fountain Financial Inc.", "His Majesty Bank Corp.", ],
                multiselect=False,
                value="Bastion Banks"
                )

            transactionAmount = gr.Slider(label="Transaction amount", minimum=0, maximum=80, step=1, randomize=True)
            
            transactionFailed = gr.Radio(
                label="Transaction failed",
                choices=[True, False],
                value=True
                )
            
            emailDomain = gr.Radio(
                label="Email domain",
                choices=["biz", "com", "info", "net", "org", "weird"],
                value="com"
                )
            
            emailProvider = gr.Radio(
                label="Email provider",
                choices=["gmail", "hotmail", "yahoo", "weird", "other"],
                value="gmail"
                )
            
            customerIPAddressSimplified = gr.Radio(
                label="Customer IP address",
                choices=["digits_and_letters", "only_numbers"],
                value="only_numbers"
                )
            
            sameCity = gr.Radio(
                label="Same city",
                choices=["no", "yes", "unknown"],
                value="no"
                )


        with gr.Column():

            gr.Markdown(
                """
                ## Predicción
                """
            )

            label = gr.Label(label="¿ FRAUDE ?")
            predict_btn = gr.Button(value="Evaluar")
            predict_btn.click(
                predict_fraud_customer,
                inputs=[
                    orderAmount,
                    orderState,
                    paymentMethodRegistrationFailure,
                    paymentMethodType,
                    paymentMethodProvider,
                    paymentMethodIssuer,
                    transactionAmount,
                    transactionFailed,
                    emailDomain,
                    emailProvider,
                    customerIPAddressSimplified,
                    sameCity,
                ],
                outputs=[label],
                api_name="prediccion"
            )
            
    gr.Markdown(
        """
        <p style='text-align: center'>
            <a href='https://www.escueladedatosvivos.ai/cursos/bootcamp-de-data-science' 
                target='_blank'>Proyecto demo creado para PROYECTO FINAL del bootcamp de EDVAI 🤗
            </a>
        </p>
        """
    )

demo.launch(share=True)
