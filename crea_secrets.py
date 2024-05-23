#import streamlit as st
import toml

output_file=".streamlit/secrets.toml"

with open("primera-base-5bb2f-firebase-adminsdk-2ch28-b147cbc93b.json") as json_file:
    json_text=json_file.read()

    config={"textkey":json_text}
    toml_config=toml.dumps(config)

    with open(output_file,"w") as target:
        target.write(toml_config)