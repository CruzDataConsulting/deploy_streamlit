#mi codigo
#import streamlit as st
#import pandas as pd
#from google.cloud import firestore
#path="https://raw.githubusercontent.com/CruzDataConsulting/appweb1/master/"#dataset.csv"
#path2="C:/Users/hdcb1/OneDrive/Documentos/SeniorDataSciense/"
# para acceder mediante credenciales
#cred=credentials.Certificate(path2+"primera-base-5bb2f-firebase-adminsdk-2ch28-b147cbc93b.json")
#firebase_admin.initialize_app(cred)

#el nuevo codigo
import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
#db = firestore.Client(credentials=creds, project="names-project-demo")
db = firestore.Client(credentials=creds, project="names")

#mi linea
#db=firestore.Client.from_service_account_json(path2+"primera-base-5bb2f-firebase-adminsdk-2ch28-b147cbc93b.json")
#db=firestore.Client.from_service_account_json("primera-base-5bb2f-firebase-adminsdk-2ch28-b147cbc93b.json")

dbNames=db.collection("names")
st.header("Nuevo registro")

index=st.text_input("Index: ")
name=st.text_input("Nombre: ")
sex=st.selectbox("Elige sexo: ",('M','F','Otro'))

submit=st.button("Crear nuevo registro")

# rutina de append en firebase
if index and name and sex and submit:
    doc_ref=db.collection("names").document(name)
    doc_ref.set({
        "index":index,
        "name":name,
        "sex":sex
    })

st.sidebar.write("Registro añadido correctamente")

# seccion de read en firebase
names_ref=list(db.collection(u'names').stream())
names_dict=list(map(lambda x: x.to_dict(), names_ref))
names_dataframe=pd.DataFrame(names_dict)
st.dataframe(names_dataframe)

#seccion delete en firebase
def loadByName(name):
    names_ref=dbNames.where(u'name', u'==', name)
    currentName=None
    for myname in names_ref.stream():
        currentName=myname
    return currentName

st.sidebar.subheader("Buscar nombre")
nameSearch=st.sidebar.text_input("nombre")
btnFiltrar=st.sidebar.button("Buscar")

if btnFiltrar:
    doc=loadByName(nameSearch)
    if doc is None:
        st.sidebar.write(f"{nameSearch} Nombre no existe")
    else:
        st.sidebar.write(doc.to_dict())
#boton eliminar
st.sidebar.markdown("----")
btnEliminar=st.sidebar.button("Eliminar")

if btnEliminar:
    deletename=loadByName(nameSearch)
    if deletename is None:
        st.sidebar.write(f"{nameSearch} Nombre no existe")
    else:
        dbNames.document(deletename.id).delete()
        st.sidebar.write(f"{nameSearch} Eliminado")

#seccion actualizar
st.sidebar.markdown("----")
newname=st.sidebar.text_input("Actualizar nombre")
btnActualizar=st.sidebar.button("Actualizar")

if btnActualizar:
    updatename=loadByName(nameSearch)
    if updatename is None:
        st.write(f"{nameSearch} No exite")
    else:
        myupdate=dbNames.document(updatename.id)
        myupdate.update(
            {
                "name":newname
                }
                )