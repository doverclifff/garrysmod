import ollama as ol
from pydantic import ValidationError
from validation import models as e2model

MODEL = "granite4.1:3b-q8_0"

src_lines: list = []
with open("./examples/library.txt", "r") as f:
    for line in f:
        if line.startswith("function"):
            src_lines.append(line.strip("\n"))

print(f"Found {len(src_lines)} lines with function declarations.")

resp_schema = e2model.E2FunctionDefinition.model_json_schema()

instructions = "From the following function declaration, extract the function identifier, returned type, argument names, and argument types."

for idx, line in enumerate(src_lines):
    try:
        query = f"{instructions}\n\n{line}"
        messages = [{"role": "user", "content": query}]
        response = ol.chat(model=MODEL, messages=messages, format=resp_schema)

        print(f"[{idx + 1}/{len(src_lines)}]\n| {'input:':<8}{line}")
        for attempt in range(5):
            print(f"| attempt #{attempt}:")
            try:
                valid_response = e2model.E2FunctionDefinition.model_validate_json(
                    response.message.content
                )
                print(f"| {'output:':<8}{valid_response}")
                break
            except ValidationError as _:
                pass

    except KeyboardInterrupt:
        break
