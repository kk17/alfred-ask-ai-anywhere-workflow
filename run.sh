#!/usr/bin/env bash

set -euo pipefail
XTRACE=${XTRACE:-false}
if [ "$XTRACE" = "true" ]; then
    set -x
fi
IFS=$'\n\t'
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd "$DIR"

PYTHON_ENV=${PYTHON_ENV:-"/usr/bin/python3"}
SCRIPT_PATH=${SCRIPT_PATH:-"ask_ai.py"}
OPTIONS_STRING=${OPTIONS_STRING:-"continue-writing#translate chinese"}
MODEL_PROVIDERS=${MODEL_PROVIDERS:-"openai_text-davinci-003"}
GOLBAL_OPT_STR=${GOLBAL_OPT_STR:-"--result-to-clipboard"}

IFS=' ' read -r -a GOLBAL_OPTS <<< "${GOLBAL_OPT_STR}"
# bash script to determine if OPTIONS_STRING_NO_PROMPT variable contain `#` symbal
FINAL_CONTENT="${CONTENT}"
if [[ "${OPTIONS_STRING}" == *"#"* ]]; then
    OPTIONS_STRING_NO_PROMPT=$(echo "${OPTIONS_STRING}" | cut -d# -f1)
    PROMPT=$(echo "${OPTIONS_STRING}" | cut -d# -f2)
    IFS=' ' read -r -a OPTS <<< "${OPTIONS_STRING_NO_PROMPT}"
    FINAL_CONTENT="${PROMPT} ${CONTENT}"
else
    IFS=' ' read -r -a OPTS <<< "${OPTIONS_STRING}"
fi

MODEL_PROVIDER_OPTIONS=()
while read LINE; do
    if [[ -n "$LINE" ]]; then
        MODEL_PROVIDER_OPTIONS+=("--model-provider")
        MODEL_PROVIDER_OPTIONS+=("$LINE")
    fi
done < <(echo -e "${MODEL_PROVIDERS}" | grep "^[^#]")

$PYTHON_ENV $SCRIPT_PATH ${MODEL_PROVIDER_OPTIONS[@]}  ${GOLBAL_OPTS[@]} ${OPTS[@]} "${FINAL_CONTENT}"
