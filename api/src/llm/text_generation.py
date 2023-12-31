from __future__ import annotations

from pathlib import Path

from llama_cpp import Llama
from src.utils import utils

LLM = None


def _find_model(model_dir=utils.config()["model"]["dir"], pattern="*.bin"):
    model_path = Path(model_dir)
    model_file_path = list(model_path.glob(pattern))[0]

    return str(model_file_path.resolve())


def _get_generation_params(params=utils.config()["model"]):
    generation_params = {
        "max_tokens": params["max_tokens"],
        "stop": params["stop"],
        "echo": params["echo"],
    }
    return generation_params


def _format_prompt(prompt):
    # remove trailing spaces
    prompt = prompt.strip()
    # remove trailing question mark
    prompt = prompt[:-1] if prompt[-1] == "?" else prompt
    return f"Q:{prompt}? A:"


def text_generation(prompt):
    global LLM
    if LLM is None:
        LLM = Llama(_find_model())

    return LLM(_format_prompt(prompt), **_get_generation_params())


def text_generation_stream(prompt):
    global LLM
    if LLM is None:
        LLM = Llama(_find_model())

    return LLM(_format_prompt(prompt), stream=True, **_get_generation_params())
