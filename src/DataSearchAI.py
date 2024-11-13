import os
import asyncio
from dotenv import load_dotenv
from openai import AzureOpenAI

printFullResponse = False

async def main():
    try:
        load_dotenv()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
        azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")

     client = AzureOpenAI(
        azure_endpoint = azure_oai_endpoint,
        azure_key = azure_oai_key,
        api_version = "2024-11-10-preview"
     )

     while True:
        print('\n1: Add comments to my code\n' +
        '2: Write unit tests\n' +
        '\"quit\" To Exit the program\n')

        command = input('Enter a number to select the task')

        if command.lower() = 'quit':
            print('Exiting Program ...')
            break

         user_input = input('\n Enter a Prompt: ')
         if command = '1' or command == '2':
            file = open(file = "../sample-code/function/function.py",encoding="utf8")
         elif command = '3':
            file = open(file = "../sample-code/function/function.py",encoding="utf8")
         else :
            print("Invalid input, please try Again")
            continue
         prompt = user_input + file
