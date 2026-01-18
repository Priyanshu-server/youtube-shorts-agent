from langchain_openai.chat_models import ChatOpenAI
from .cust_types import Model


def get_model(model_name: str, model_parent: str, *model_args, **model_kwargs) -> Model:
    model = None
    if model_parent == "openai":
        model = get_openai_model(model_name, *model_args, **model_kwargs)
    else:
        raise ValueError(f"Unsupported model parent: {model_parent}")

    return Model(model_name=model_name, model_parent=model_parent, model=model)


def get_openai_model(model_name, *args, **kwargs) -> ChatOpenAI:
    """Returns an instance of ChatOpenAI with the specified model name and parameters."""
    return ChatOpenAI(name=model_name, *args, **kwargs)
