import httpx, os, json, subprocess, atexit

url = 'https://generativelanguage.googleapis.com/v1beta/interactions'

headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': os.environ["API_KEY"]
}


history = []

def append_user_request(history, new_question):
    history.append({ "type": "user_input", "content": [{ "type": "text", "text": new_question }] })
    return

tool_definition_string = '''
you are a smart agent capible of running external tools acourding to the defintion bellow

tool calling:
```json
{"type": "run_command", "command": "<command_name>"}
```

response:
```json
{"type": "response", "command_output": "<command_output>"}
```

for example to run "ls" you would say:
```json
{"type": "run_command", "command": "ls"}
```

and the expected resoponse is:
```json
{"type": "response", "command_output": "Desktop Documents Downloads"}
```

you will only run tools when you are asked otherwise you answer the users questions
'''

def send_text_to_ai(text_to_send):
    append_user_request(history, text_to_send)

    payload = {
        "store": False,
        "model": "gemini-3.5-flash-lite",
        "input": history
    }

    response = httpx.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    
    history.extend(response.json()["steps"])
    
    return response.json()["steps"][1]["content"][-1]["text"]
    #print(json.dumps(response.json(), indent=2))
    #print(response.json()["steps"][1]["content"][-1]["text"] + "\n")

def check_for_tool_call(ai_output):
    tool_call_string = ""
    inside_tool_call = False
    for line in ai_output.splitlines():

        if line.startswith("```"):
            # check for start of a tool call
            if inside_tool_call == False:
                inside_tool_call = not inside_tool_call
                continue

            # check for end of the first tool call
            if inside_tool_call == True:
                break


        # collect tool call in a string
        if inside_tool_call:
            tool_call_string += line

    if tool_call_string != "":
        tool_call = json.loads(tool_call_string)["command"]
        return tool_call
    else:
        return None


def stop_sandbox():
    subprocess.run(["podman", "rm", "-f", "-t", "0", "agent-box"], capture_output=True)

def start_sandbox():
    stop_sandbox()                                  # clear any leftover container
    subprocess.run([
        "podman", "run", "-d", "--name", "agent-box",
        "--network", "none",
        "--read-only", "--tmpfs", "/tmp",
        "--memory", "512m", "--cpus", "1", "--pids-limit", "100",
        "--cap-drop", "all", "--security-opt", "no-new-privileges",
        "-v", "/home/ahmed/dev/AI-agent/sandbox:/work", "-w", "/work",
        "docker.io/library/alpine:latest", "sleep", "infinity",
    ], check=True, capture_output=True)
    atexit.register(stop_sandbox)                   # clean up when the script exits

def run_in_sandbox(command):
    try:
        r = subprocess.run(
            ["podman", "exec", "agent-box", "timeout", "30", "sh", "-c", command],
            capture_output=True, text=True, timeout=40)
    except subprocess.TimeoutExpired:
        return format({"type": "response", "error": "timed out after 30s"})
    output = (r.stdout + r.stderr)[-2000:]
    if r.returncode != 0:
        return format({"type": "response", "error": f"exit code {r.returncode}: {output}"})
    return format({"type": "response", "command_output": output})


print("sending tool defintion: " + "\n" + tool_definition_string)
response = send_text_to_ai(tool_definition_string)
print(response)
start_sandbox()

while True:
    try:
        question = input("ask anything? \n")
    except (EOFError, KeyboardInterrupt):
        print("Bye\n")
        break

    text_response = send_text_to_ai(question)

    tool_call_string = check_for_tool_call(text_response)

    ### tool running loop
    while tool_call_string:
        print("\n\n### Ai is running '" + tool_call_string + "'")
        tool_call_result = run_in_sandbox(tool_call_string)
        print("\n\n### tool result '" + tool_call_result + "'")
        text_response = send_text_to_ai(tool_call_result)
        tool_call_string = check_for_tool_call(text_response)

    print(text_response + "\n")

