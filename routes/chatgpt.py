from flask import Blueprint, request
import os
import json
import responses
from openai import OpenAI
import requests
from config.chatgpt_config import SYSTEM_RULES, TOOLS

openai_bp = Blueprint('openai', __name__)

@openai_bp.route('/health')
def openai_index():
    return responses.Ok200("success", "API chatgpt is working")

@openai_bp.route('/4o-mini', methods=['POST'])
def chatgpt_4o():
    data = request.get_json()
    if not data:
        return responses.Error400("error", "Dados JSON não fornecidos")

    messages_param = data.get("messages")
    system_rules = data.get("system_rules", SYSTEM_RULES)
    tools_param = data.get("tools", TOOLS)
    if messages_param is None:
        return responses.Error400("error", "Parâmetro 'messages' é obrigatório")
    if isinstance(messages_param, list):
        messages = messages_param
    else:
        try:
            messages = json.loads(messages_param)
        except Exception as e:
            return responses.Error400("error", f"Erro ao desserializar mensagens: {e}")
    functions = []
    if isinstance(tools_param, list):
        functions = tools_param
    else:
        try:
            functions = json.loads(tools_param)
        except Exception as e:
            return responses.Error400("error", f"Erro ao desserializar tools: {e}")
    if functions == []:
        functions = None
        tools = None
    else:
        tools = [{"type": "function", "function": func} for func in functions]

    messages.append({
        "role": "system",
        "content": system_rules
    })
    api_key = os.getenv("OPENAI_API_KEY", "SEM_TOKEN")
    if not api_key or api_key == "SEM_TOKEN":
        return responses.Error500("Por favor, defina a variável de ambiente OPENAI_API_KEY", None)

    client = OpenAI(
        api_key=api_key,
    )

    def substitute_placeholders(item, payload: dict):
        import re
        if isinstance(item, str):
            return re.sub(r'\$\(([^)]+)\)', lambda m: str(payload.get(m.group(1).strip(), m.group(0))), item)
        elif isinstance(item, dict):
            return {k: substitute_placeholders(v, payload) for k, v in item.items()}
        elif isinstance(item, list):
            return [substitute_placeholders(elem, payload) for elem in item]
        return item

    try:
        while True:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools
            )
            if response.choices[0].message.tool_calls:
                for tool_call in response.choices[0].message.tool_calls:
                    functionJson = [item for item in tools if item.get("function", {}).get("name") == tool_call.function.name]
                    
                    if functionJson[0].get("function", {}).get("ziap", {}).get("type", {}) == "api":
                        apiData = functionJson[0].get("function").get("ziap")
                        api_method = apiData.get("method", "GET").upper()
    
                        payload = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
                        
                        processed_endpoint = substitute_placeholders(apiData.get("endpoint", ""), payload)
                        processed_headers = substitute_placeholders(apiData.get("headers", {}), payload)
                        processed_cookies = substitute_placeholders(apiData.get("cookies", {}), payload)
                        processed_body = substitute_placeholders(apiData.get("body", {}), payload)
                        
                        if api_method in ["POST", "PUT"]:
                            try:
                                result = requests.request(apiData["method"], processed_endpoint, json=processed_body, headers=processed_headers, cookies=processed_cookies, verify=False, timeout=500).text
                            except Exception as e:
                                result = str(e)
                        elif api_method in ["GET", "DELETE"]:
                            try:
                                result = requests.request(apiData["method"], processed_endpoint, headers=processed_headers, cookies=processed_cookies, verify=False, timeout=500).text
                            except Exception as e:
                                result = str(e)
                    elif functionJson[0].get("function", {}).get("ziap", {}).get("type", {}) == "default":
                        if tool_call.function.name == "execCommand":
                            import subprocess
                            try:
                                json_args = json.loads(tool_call.function.arguments)
                                print(f"\n\n// Executando: {json_args.get('command')}")
                                result = subprocess.check_output(json_args.get("command"), shell=True, text=True)
                                messages.append({
                                    "role": "assistant",
                                    "content": f"Comando executado: {json_args.get('command')}\nResultado:\n{result}"
                                })
                            except subprocess.CalledProcessError as e:
                                result = f"Erro ao executar comando: {str(e)}"
                                messages.append({
                                    "role": "assistant",
                                    "content": f"Erro ao executar comando: {json_args.get('command')}\n{str(e)}"
                                })
                        else:
                            result = "Função não implementada"
                    else:
                        result = "Função não implementada"
                    
                    messages.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [tool_call]
                    })
                    print(result)
                    print(f"//\ Fim: {json_args.get('command')}")
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })
                continue
            break
    
        message = response.choices[0].message.content
        return responses.Ok200("success", message)
    except Exception as e:
        print(f"Erro ao processar requisição: {e}")
        return responses.Error500("Erro ao processar requisição", str(e))