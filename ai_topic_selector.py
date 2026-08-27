from pathlib import Path
from random import sample
from re import findall
def Categorizing(content):
    topic_and_path = {file[:-4]:str(Path(root) / file) for root, dirs , files in Path('symbols').walk() for file in files}
    try:
        from ollama import chat
        topic_set = set(topic_and_path.keys())
        prompt_base = f'You are an expert in categorizing scientific content. I will send you a piece of scientific content and ask for your help in identifying its subject matter. I will provide a list of permitted topics, and I would like you to select topics relevant to the text. Please note these rules: 1: your response must include just the names. nothing more is acceptable. 2: you must select between 3 and 5 topic.  3: Important: Do NOT use synonyms or related terms. You MUST copy the exact names from the list below. If a concept matches something, but that things is not in the list, you must choose the closest existing name from the list or skip it. Only output the exact strings provided in the list. \n permitted topics: \n {topic_set}'
        special_prompt = f'now, categorize this content: \n {content}'
        messages = [{'role': 'system', 'content': prompt_base},{'role': 'user', 'content': special_prompt}]
        AI_respone = chat(model= 'gemma3:4b', messages= messages ,options={"temperature": 0.0})
        for x in range(3):
            AI_result = str(AI_respone.message.content).split()
            if len(set(AI_result).intersection(topic_set)) < 3:
                print("Invalid response (rule 3):", AI_respone.message.content)
                messages.append({'role':'user','content':f'You have used these topics, but they are not on the approved list: {set(AI_result).difference(topic_set)} Try harder, and this time, use *only* the approved list.'})
                AI_respone = chat(model= 'gemma3:4b', messages= messages ,options={"temperature": 0.0})
            else:
                break
        if len(set(AI_result).intersection(topic_set)) < 3:
            general_science = ({findall(r'symbols[\\/](.*)',str(root))[0]:files for root, dirs , files in Path('symbols').walk() if (findall(r'symbols[\\/](.*)',str(root)))!= []}.get('general_science'))
            random_result = sample(general_science, k=3)
            return[topic_and_path.get(topic[:-4]) for topic in random_result]
        return[topic_and_path.get(topic) for topic in set(AI_result).intersection(topic_set)]
    except Exception as e:
        print("Error occurred:", e)
        general_science = ({findall(r'symbols[\\/](.*)',str(root))[0]:files for root, dirs , files in Path('symbols').walk() if findall(r'symbols[\\/](.*)',str(root))!= []}.get('general_science'))
        random_result = sample(general_science, k=3)
        return[topic_and_path.get(topic[:-4]) for topic in random_result]

with open('science_quotes.txt','r',encoding='utf-8') as sq:
    print(Categorizing(sq.read()))