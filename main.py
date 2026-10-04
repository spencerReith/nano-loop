"""
main.py

core query loop
"""

from llm import invoke_llm 
from dotenv import load_dotenv 

load_dotenv()

msg_history = []

system_prompt = "You answer everything extremely clearly and concisely"
msg_history.append({"role": "system", "content": system_prompt})



def chat_loop():
    user_msg = input("\nUser: ")
    msg_history.append({"role": "user", "content": user_msg})
    llm_msg = invoke_llm(msg_history)
    msg_history.append(llm_msg)
    chat_loop()

chat_loop()