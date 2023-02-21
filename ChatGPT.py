import util
import os
import openai

credentials = util.getCredentials()
sysPath = os.getcwd() + "/"


def Ask(stringtofind):
    openai.api_key = credentials['OPENAI_API_KEY']
    start_sequence = "\nA:"
    restart_sequence = "\n\nQ: "

    response = openai.Completion.create(
    model="text-davinci-003",
    #prompt="I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".\n\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955?\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\nQ: Where were the 1992 Olympics held?\nA: The 1992 Olympics were held in Barcelona, Spain.\n\nQ: How many squigs are in a bonk?\nA: Unknown\n\nQ:",
    prompt=stringtofind+"\nA",
    temperature=0,
    max_tokens=500,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["\n"]
    )
    textdata = ''
    for result in response.choices:
        textdata = result.text
    #return response
    
    return result.text


def Rewrite(stringtofind):
    openai.api_key = credentials['OPENAI_API_KEY']
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f'Rewrite these sentense with another words in portuguese, do not include dates,weekdays or years and be like human:\n\n{stringtofind}',
    temperature=0.5,
    max_tokens=500,
    top_p=1,
    frequency_penalty=0.8,
    presence_penalty=0
    )
    textdata = ''
    for result in response.choices:
        textdata += result.text   
    return result.text
    #return textdata    
def removigStrin(datastring):

    return datastring