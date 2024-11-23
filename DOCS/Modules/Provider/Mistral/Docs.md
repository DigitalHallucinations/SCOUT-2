chat endpoint:

curl --location "https://api.mistral.ai/v1/chat/completions" \
     --header 'Content-Type: application/json' \
     --header 'Accept: application/json' \
     --header "Authorization: Bearer $MISTRAL_API_KEY" \
     --data '{
    "model": "Mistral AI generative model",
    "messages": [{"role": "user", "content": "Who is the most renowned French painter?"}]
  }'

embeddings endpoint:

curl --location "https://api.mistral.ai/v1/embeddings" \
     --header 'Content-Type: application/json' \
     --header 'Accept: application/json' \
     --header "Authorization: Bearer $MISTRAL_API_KEY" \
     --data '{
    "model": "mistral-embed",
    "input": ["Embed this sentence.", "As well as this one."]
  }'

Endpoints and benchmarks
We provide five different API endpoints to serve our generative models with different price/performance tradeoffs and one embedding endpoint for our embedding model.

Mistral AI generative models
Mistral AI provides five API endpoints for its five Large Language Models:

open-mistral-7b (aka mistral-tiny-2312)
open-mixtral-8x7b (aka mistral-small-2312)
mistral-small-latest (aka mistral-small-2402)
mistral-medium-latest (aka mistral-medium-2312)
mistral-large-latest (aka mistral-large-2402)
All models have a 32K token context window size.

Mistral AI embedding model
Embedding models enable retrieval and retrieval-augmented generation applications.

Mistral AI embedding endpoint outputs vectors in 1024 dimensions. It achieves a retrieval score of 55.26 on MTEB.

API name: mistral-embed



Chat completions

PYTHON

No streaming
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = MistralClient(api_key=api_key)

messages = [
    ChatMessage(role="user", content="What is the best French cheese?")
]

# No streaming
chat_response = client.chat(
    model=model,
    messages=messages,
)

print(chat_response.choices[0].message.content)

With streaming
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = MistralClient(api_key=api_key)

messages = [
    ChatMessage(role="user", content="What is the best French cheese?")
]

# With streaming
stream_response = client.chat_stream(model=model, messages=messages)

for chunk in stream_response:
    print(chunk.choices[0].delta.content)

With async
from mistralai.async_client import MistralAsyncClient
from mistralai.models.chat_completion import ChatMessage

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = MistralAsyncClient(api_key=api_key)

messages = [
    ChatMessage(role="user", content="What is the best French cheese?")
]

# With async
async_response = client.chat_stream(model=model, messages=messages)

async for chunk in async_response: 
    print(chunk.choices[0].delta.content)

CURL

curl --location "https://api.mistral.ai/v1/chat/completions" \
     --header 'Content-Type: application/json' \
     --header 'Accept: application/json' \
     --header "Authorization: Bearer $MISTRAL_API_KEY" \
     --data '{
    "model": "mistral-large-latest",
    "messages": [
     {
        "role": "user",
        "content": "What is the best French cheese?"
      }
    ]
}'


Embeddings

PYTHON

from mistralai.client import MistralClient

api_key = os.environ["MISTRAL_API_KEY"]
client = MistralClient(api_key=api_key)

embeddings_batch_response = client.embeddings(
      model="mistral-embed",
      input=["Embed this sentence.", "As well as this one."],
)

CURL

curl --location "https://api.mistral.ai/v1/embeddings" \
  --header 'Content-Type: application/json' \
  --header 'Accept: application/json' \
  --header "Authorization: Bearer $MISTRAL_API_KEY" \
  --data '{
 "model": "mistral-embed",
 "input": [
   "Embed this sentence.", 
   "As well as this one."
 ]
}'


JSON mode

PYTHON

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = MistralClient(api_key=api_key)

messages = [
    ChatMessage(role="user", content="What is the best French cheese? Return the product and produce location in JSON format")
]

chat_response = client.chat(
    model=model,
    response_format={"type": "json_object"},
    messages=messages,
)

print(chat_response.choices[0].message.content)

Curl

curl --location "https://api.mistral.ai/v1/chat/completions" \
     --header 'Content-Type: application/json' \
     --header 'Accept: application/json' \
     --header "Authorization: Bearer $MISTRAL_API_KEY" \
     --data '{
    "model": "mistral-large-latest",
    "messages": [
     {
        "role": "user",
        "response_format": {"type": "json_object"},
        "content": "What is the best French cheese? Return the product and produce location in JSON format"
      }
    ]
  }'

Create Chat Completions
REQUEST BODY SCHEMA: application/json
required
model
required
string
ID of the model to use. You can use the List Available Models API to see all of your available models, or see our Model overview for model descriptions.

messages
required
Array of objects
The prompt(s) to generate completions for, encoded as a list of dict with role and content. The first prompt role should be user or system.

temperature	
number or null [ 0 .. 1 ]
Default: 0.7
What sampling temperature to use, between 0.0 and 1.0. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.

We generally recommend altering this or top_p but not both.

top_p	
number or null [ 0 .. 1 ]
Default: 1
Nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

max_tokens	
integer or null >= 0
Default: null
The maximum number of tokens to generate in the completion.

The token count of your prompt plus max_tokens cannot exceed the model's context length.

stream	
boolean or null
Default: false
Whether to stream back partial progress. If set, tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.

safe_prompt	
boolean
Default: false
Whether to inject a safety prompt before all conversations.

random_seed	
integer
Default: null
The seed to use for random sampling. If set, different calls will generate deterministic results.

Responses
200
OK


POST
/chat/completions
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"model": "mistral-tiny",
"messages": [
{}
],
"temperature": 0.7,
"top_p": 1,
"max_tokens": 16,
"stream": false,
"safe_prompt": false,
"random_seed": null
}
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"id": "cmpl-e5cc70bb28c444948073e77776eb30ef",
"object": "chat.completion",
"created": 1702256327,
"model": "mistral-tiny",
"choices": [
{}
],
"usage": {
"prompt_tokens": 14,
"completion_tokens": 93,
"total_tokens": 107
}
}
Create Embeddings
REQUEST BODY SCHEMA: application/json
required
model	
string
The ID of the model to use for this request.

input	
Array of strings
The list of strings to embed.

encoding_format	
string
Value: "float"
The format of the output data.

Responses
200
OK

RESPONSE SCHEMA: application/json
id
required
string
object
required
string
data
required
Array of objects
model
required
string
usage
required
object

POST
/embeddings
Request samples
Payload
Content type
application/json

Copy
Expand allCollapse all
{
"model": "mistral-embed",
"input": [
"Hello",
"world"
],
"encoding_format": "float"
}
Response samples
200
Content type
application/json

Copy
Expand allCollapse all
{
"id": "embd-aad6fc62b17349b192ef09225058bc45",
"object": "list",
"data": [
{},
{}
],
"model": "string",
"usage": {
"prompt_tokens": 9,
"total_tokens": 9
}
}
List Available Models
Responses
200
OK

RESPONSE SCHEMA: application/json
object
required
string
data
required
Array of objects (Model)

Function Calling Schema

tools = [
    {
        "type": "function",
        "function": {
            "name": "tool 1",
            "description": "description of tool",
            "parameters": {
                "type": "object",
                "properties": {
                    "transaction_id": {
                        "type": "string",
                        "description": "description of param",
                    }
                },
                "required": [param if required],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tool 2",
            "description": "description of tool",
            "parameters": {
                "type": "object",
                "properties": {
                    "transaction_id": {
                        "type": "string",
                        "description": "param discription",
                    }
                },
                "required": [param if required],
            },
        },
    }
]

import functools

names_to_functions = {
    'Tool 1': functools.partial(Tool 1, required param if any),
    'Tool 2': functools.partial(Tool 2, required param if any)
}

tool_choice
Users can use tool_choice to speficy how tools are used:

"auto": default mode. Model decides if it uses the tool or not.
"any": forces tool use.
"none": prevents tool use.
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

model = "mistral-large-latest"
api_key="TYPE YOUR API KEY"

client = MistralClient(api_key=api_key)
response = client.chat(model=model, messages=messages, tools=tools, tool_choice="auto")
response

Mistral model identifies there are information missing and responds that “I need the transaction id to check the status. Could you please provide me with the transaction id?”.

ChatCompletionResponse(id='dca45f6bdc284d48bc13acfdb6e2f980', object='chat.completion', created=1707931630, model='mistral-large', choices=[ChatCompletionResponseChoice(index=0, message=ChatMessage(role='assistant', content='I need the transaction id to check the status. Could you please provide me with the transaction id?', name=None, tool_calls=[]), finish_reason=<FinishReason.stop: 'stop'>)], usage=UsageInfo(prompt_tokens=173, total_tokens=193, completion_tokens=20))

Let’s add this message to the messages list and then add another user message providing the transaction ID: “My transaction ID is T1001.”

messages.append(ChatMessage(role="assistant", content=response.choices[0].message.content))
messages.append(ChatMessage(role="user", content="My transaction ID is T1001."))

Running the Mistral model again, we get the response including tool_calls with the chosen function name retrieve_payment_status and the arguments for this function.

response = client.chat(model=model, messages=messages, tools=tools, tool_choice="auto")
response

Output:

ChatCompletionResponse(id='9ec8d47af52d4c258c641a7d9f62336e', object='chat.completion', created=1707931630, model='mistral-large', choices=[ChatCompletionResponseChoice(index=0, message=ChatMessage(role='assistant', content='', name=None, tool_calls=[ToolCall(id='null', type=<ToolType.function: 'function'>, function=FunctionCall(name='retrieve_payment_status', arguments='{"transaction_id": "T1001"}'))]), finish_reason=<FinishReason.stop: 'stop'>)], usage=UsageInfo(prompt_tokens=211, total_tokens=250, completion_tokens=39))

Let’s add the response message to the messages list.

messages.append(response.choices[0].message)

execute function call

Let’s extract some useful function information from model response including function_name and function_params. It’s clear here that our Mistral model has chosen to use the function retrieve_payment_status with the parameter transaction_id set to T1001.

import json

tool_call = response.choices[0].message.tool_calls[0]
function_name = tool_call.function.name
function_params = json.loads(tool_call.function.arguments)
print("\nfunction_name: ", function_name, "\nfunction_params: ", function_params)

Output

function_name:  retrieve_payment_status 
function_params: {'transaction_id': 'T1001'}

Now we can execute the function and we get the function output '{"status": "Paid"}'.

function_result = names_to_functions[function_name](**function_params)
function_result

Output

'{"status": "Paid"}'

Generate final answer

messages.append(ChatMessage(role="tool", name=function_name, content=function_result))

response = client.chat(model=model, messages=messages)
response.choices[0].message.content

Output:

The status of your transaction with ID T1001 is "Paid". Is there anything else I can assist you with?