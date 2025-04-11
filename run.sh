#!/usr/bin/env bash

set -euo pipefail
XTRACE=${XTRACE:-false}
if [ "$XTRACE" = "true" ]; then
    set -x
fi
IFS=$'\n\t'
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd "$DIR"

PYTHON_ENV=${PYTHON_ENV:-"python3"}
SCRIPT_PATH=${SCRIPT_PATH:-"ask_ai.py"}
OPTIONS_STRING=${OPTIONS_STRING:-"continue-writing#translate chinese"}
AAA_LM_MODEL=${AAA_LM_MODEL:-"openrouter/google/gemini-2.0-flash-lite-preview-02-05:free"}
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
MODEL_PROVIDER_OPTIONS+=("--model")
MODEL_PROVIDER_OPTIONS+=("$AAA_LM_MODEL")


$PYTHON_ENV $SCRIPT_PATH ${MODEL_PROVIDER_OPTIONS[@]}  ${GOLBAL_OPTS[@]} ${OPTS[@]} "${FINAL_CONTENT}"
