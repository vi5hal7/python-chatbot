import openai
import gradio
openai.api_base="https://api.pawan.krd/unfiltered/v1"

openai.api_key="pk-jwnVtziRbMsmMKDcgoleZdbbAqHyXVPUxSdgYqkFiwctOStS"

# models = openai.Model.list()
# print(models)
history=[]
first_message=True
file_name="Default"
def chat_bot(message):
    global first_message,file_name

    # message= input("Enter the message or type quit to quit::")
    # if message=="quit":
    #         break
    if first_message:
        file_name= message[:20]
        first_message = False
    history.append({"role": "user", "content": message})
    chat_completion =openai.ChatCompletion.create(
        model="gpt-4o",
        # messages=[{"role": "user", "content": message}])
        messages= history)

    response=(chat_completion.choices[0].message.content)
    history.append({"role": "assistant", "content": response})

    # print(f"Message : {message}")
    # print(f"Response : {response}")
    with open(f"{file_name}.txt",'a',encoding="utf-8") as f:
        f.write(f"Message : {message}\n")
        f.write(f"Response : {response}\n")
    conversation =[(history[i]["content"],history[i+1]["content"]) for i in range(0,len(history)-1,2)]
    return "",conversation


with gradio.Blocks() as chatbot_ui:
    gradio.Markdown("""<h1><center> My chatbot </center><h1>""")
    chatbot = gradio.Chatbot()
    txt = gradio.Textbox(show_label=False,placeholder="chat with me")
    submit=gradio.Button("Send")
    submit.click(chat_bot,inputs=txt,outputs=[txt,chatbot])

chatbot_ui.launch(share=True)
