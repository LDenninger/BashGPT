# BashGPT
This is a simple command line tool written in python utilizing the OpenAI API.
It can be used to employ different pre-defined system calls for quick help through the command line.
For further information about the API, please visit: https://openai.com/blog/openai-api

## Usage
Through the `resources/config.json` file, you can specify default parameters for the model and system calls.
The parameters can also be passed when calling BashGPT. <br/>
Example usage:
```
python BashGPT.py --model_name "gpt-3.5-turbo" --mode "assistant" --temperature 0.0 --max_tokens 500 --use_past False --top_p 1.0
```

## Disclaimer
This project is still work in progress and there is plan to add more functionalities