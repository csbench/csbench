import openai
import time


def call_gpt(llm_model_name,message,max_retries=10):
    retries = 0

    while retries < max_retries:
        try:
            chat_completion = openai.ChatCompletion.create(
            model=llm_model_name,
            messages=[{"role": "user", "content": message}]
            )
            response = chat_completion.choices[0].message.content
            retries+=1
            return response
        
        except Exception as e:
            print(f"Someting wrong:{e}. Retrying in 2 minutes...")
            time.sleep(120) 
            retries += 1

    print("Max retries reached. Unable to get a response.")
    return None

if __name__=="__main__":
    # setting
    openai.api_base = "your api"
    openai.api_key = 'your api key'
    llm_model_name='gpt-4-turbo-2024-04-09'
    output=call_gpt(llm_model_name=llm_model_name,
                        message="hello,introduce yourself")
    print(output)