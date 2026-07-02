import ollama as ol
import pydantic
import validation_models

MODEL = "granite4.1:8b-q8_0"


class E2FunctionDefinition(pydantic.BaseModel):
    name: str
    return_type: validation_models.E2Type
    arguments: dict[str, validation_models.E2Type]


resp_schema = validation_models.E2FunctionDefinition.model_json_schema()

query = "From the following function declaration, extract the function name, returned type, argument names, and argument types."
src = "function number AddAToB(A:number, B:number)"
query = f"{query}\n\n{src}"

messages = [{"role": "user", "content": query}]

response = ol.chat(model=MODEL, messages=messages, format=resp_schema)
response = E2FunctionDefinition.model_validate_json(response.message.content)
print(response)
