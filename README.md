# AI Agent Learning

I want to learn about how AI agents work, and what better way to do that that to build one myself.

---

## 📌 Project Overview

<!-- Add a brief summary of what you are building, your motivation, and your learning goals. -->
This repository documents my journey learning how AI agents work under the hood. It progressively builds up concepts:
1. Sending basic prompt requests to an LLM API.
2. Building a stateful conversational chatbot with message history.
3. Teaching an LLM to invoke external tools (commands) using custom prompts.
4. Safely executing those tools in a strictly sandboxed container environment.

---

## ⚙️ Prerequisites

Before running the scripts, ensure you have the following installed:

- **Python 3.10+**
- **[Podman](https://podman.io/)**: Required for running sandboxed commands safely.
- **Python dependencies**:
  ```bash
  pip install httpx
  ```

---

## 🔑 Getting and Setting Up the API Key

The scripts interact with Google's Gemini Interactions API (`gemini-3.5-flash-lite`).

### 1. Get an API Key
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Sign in with your Google account.
3. Click **"Get API key"** and create a new key.

### 2. Configure the Key
Set the `API_KEY` environment variable in your terminal before running any script:

```bash
export API_KEY="your-gemini-api-key-here"
```

*(Optional)* You can also store your key inside `api.key` which is ignored by .gitignore:
```bash
echo "your-gemini-api-key-here" > api.key
export API_KEY=$(cat api.key)
```

---

## 🛡️ Sandbox Isolation with Podman

When building agents capable of executing arbitrary bash commands, **sandboxing is critical** to prevent accidental damage or malicious actions on your host system.

`04-simple_tool_calling_agent.py` uses **Podman** to spin up a container (`agent-box`) with:
- `--network none`: No internet access inside the sandbox.
- `--read-only`: Read-only root filesystem.
- `--tmpfs /tmp`: Ephemeral in-memory temporary storage.
- `--cap-drop all`: Drops all Linux kernel capabilities.
- `--security-opt no-new-privileges`: Blocks privilege escalation.
- `--memory 512m --cpus 1 --pids-limit 100`: Resource exhaustion protections.
- `-v ./sandbox:/work`: Restricts file modifications strictly to the `./sandbox` folder.

### Pull the Container Image
Ensure the Alpine base image is pulled beforehand:
```bash
podman pull docker.io/library/alpine:latest
```

---

## 🚀 How to Run

### Hello World
Hello World but from an AI:
```bash
python 01-LLM_hello_world.py
```

### Stateless Chatbot
Chatbot without history, every prompt is a new chat, try telling it something then ask it about that thing:
```bash
python 02-chatbot_without_history.py
```

### Stateful Chatbot (With History)
Chat with conversation history, now try the same thing as the previous one and you will see that it remembers:
```bash
python 03-chatbot_with_history.py
```

### Tool-Calling Agent in Sandbox
How is a chatbox able to run commands, ask it to write a poem to a file:
```bash
python 04-simple_tool_calling_agent.py
```

---

## 📝 Notes & Future Learnings

<!-- Space to write down takeaways, edge cases, and future iterations (e.g., native function calling, MCP, multi-agent collaboration) -->
- [ ] Explore native Gemini function calling API.
- [ ] Add more sandbox tools (file reading, writing, python execution).
- [ ] Handle multi-step planning and reflection loops.
