import google.generativeai as genai

genai.configure(api_key="AIzaSyAbIC6MS4nqWBpk3xcT7_jbU9dII_thkAI")

for model in genai.list_models():
    print(model.name)
