import autogen
import os
from dotenv import load_dotenv
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from warehouse import get_warehouse, get_warehouse_declaration
from send_mail import send_mail,send_email_declaration
from flask import Flask, request, render_template

# Load the .env file
load_dotenv()

# Fetching the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")



# Flask app to render the chat interface
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
   if request.method == 'POST':
      image_url = request.form['image']
      customer_email = request.form['email']
      customer_message = request.form['message']
      
      initiate_chat(image_url, customer_email, customer_message)
      return render_template('result.html')
   else:
      return render_template('index.html')



# config_list is a list of dictionaries where each dictionary contains the model name and the API key
config_list = [{"model":"gpt-3.5-turbo", "api_key":api_key}]

# config list for vision model 
vision_config_list = [{"model":"gpt-4-vision-preview", "api_key":api_key}]


# Terminates the conversation if the message is "TERMINATE" 
def is_termination_msg(message):
      has_content = "content" in message and message["content"] is not None
      return has_content and "TERMINATE" in message["content"]

# user proxy ( The user proxy is the main object that you will use to interact with the assistant its like proxy to human)
# The user proxy is the main object that you will use to interact with the assistant. It acts as a proxy to the human user
user_proxy = autogen.UserProxyAgent(name = "user_proxy", system_message = "You're the boss", human_input_mode ="NEVER",
                                    is_termination_msg = is_termination_msg,
                                    function_map={"get_warehouse": get_warehouse, "send_mail": send_mail},
                                                                        code_execution_config={"use_docker": False})


# Inventory manager to manage the inventory of the automotive parts and tells user proxy to execute the get_warehouse function
inventory_manager = autogen.AssistantAgent(name = "inventory_manager", system_message="""As the inventory manager  
                                                You  provide the details of availability and pricing of the parts """, 
                                                llm_config = { "config_list" : config_list, "functions": [get_warehouse_declaration]})


# Damage analysis agent to analyze the damage of the automotive parts
damage_analyst = MultimodalConversableAgent(name = "damage_analyst", system_message="""As the damage analysis agent
                                         You are responible to analyze the damage and accurately descibe the contents of the image provided by the customer.
                                         Respond only with what is visually evident in the image. """, llm_config={ "config_list" : vision_config_list, "max_tokens":300}  )
                                         
                                         
                                         
# Customer service agent to provide customer service to the customers
customer_support_agent = autogen.AssistantAgent(name = "customer_service_agent", system_message="""You're the customer service agent and responsible for drafting
                                                emails following confirmation of inventory and pricing. Respond with "TERMINATE" to end the conversation.""",
                                                llm_config = { "seed":18, "config_list" : config_list, "functions": [send_email_declaration]})


# group chat among the agents
group_chat = autogen.GroupChat( agents=[user_proxy, inventory_manager, customer_support_agent, damage_analyst],messages=[])

# Manager to manage the group chat
group_chat_manager = autogen.GroupChatManager( groupchat=group_chat, llm_config={"config_list" : config_list})

def initiate_chat(image_url, customer_email, customer_message):
   # Initiate the group chat
   user_proxy.initiate_chat(group_chat_manager,
                           message= f"""Process overview:
                                       step 1. Damage analysis identifies the car brand and the required part (is something central, or something broken or missing)
                                       from the customer's message and images.
                                       
                                       step 2. Inventory manager just verifies the part availability in the warehouse database.
                                    
                                       step 3. Customer support agent will acts as sender by composing and send a professional response email to customer 
                                       
                                       Customer message: '{customer_message}'
                                       Customer's Email: '{customer_email}'
                                       Image Reference: '{image_url}'
                                       """
                           )


# Run the Flask app to render the chat interface
if __name__ == "__main__":
    app.run(debug=True)