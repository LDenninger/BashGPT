
#!/bin/bash
N_ARGS=$#

if [ $N_ARGS -eq 0 ]; then
    COMMAND="help"
else
    COMMAND=$1
    N_ARGS=$(expr $N_ARGS - 1) 
    shift
fi

case "$COMMAND" in
    ask)
      QUESTION="$*"
      python3 src/gpt.py --ask --question "$QUESTION" | pandoc -f markdown -t plain | cat
      #pandoc -f markdown -t plain <(python3 src/gpt.py --ask --question "$QUESTION") | cat
      #python3 src/gpt.py --ask --question "$QUESTION" > /tmp/output.md && pandoc /tmp/output.md -f markdown -t plain | cat && rm /tmp/output.md

      ;;

    set)
      if [ $N_ARGS -le 1 ]; then
          echo "Please provide configuration key and value like: gpt set [key] [value]"
          exit -1
      fi

      KEY=$1
      VALUE=$2

      python3 src/gpt.py --set --key $KEY --value $VALUE
      ;;

    set_key)
      if [ $N_ARGS -eq 0 ]; then
          echo "Please provide configuration key and value like: gpt set_key [value]"
          exit -1
      fi
      echo "Setting new OpenAI Api key: $1"
      echo "export OPENAI_API_KEY=$1" >> ~/.bashrc
      echo "export OPENAI_API_KEY=$1" >> ~/.zshrc
      echo "Please source .bashrc or .zshrc again"

      ;;

    help)
      echo "Usage: kal [command]"
      echo "Commands:"
      echo "  ask    - Ask a question"
      echo "  set    - Set a value"
      echo "  help   - Show this help message"
      ;;

    *)
      echo "Unknown command: $COMMAND"
      echo "Use 'kal help' for usage information."
      ;;
esac