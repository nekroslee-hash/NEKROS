import pytest

from nekros.orchestrator import ProviderNotConfigured, choose_free_model


def test_only_free_models_are_selected():
    assert choose_free_model("سلام", ["provider/model-paid", "provider/model-free:free"]) == "provider/model-free:free"


def test_paid_model_is_never_selected():
    with pytest.raises(ProviderNotConfigured):
        choose_free_model("سلام", ["provider/model-paid"])


def test_code_task_prefers_coding_model():
    models = ["provider/general:free", "qwen/qwen-coder:free"]
    assert choose_free_model("این کد پایتون را اصلاح کن", models) == "qwen/qwen-coder:free"


def test_reasoning_task_prefers_reasoning_model():
    models = ["provider/general:free", "deepseek/deepseek-r1:free"]
    assert choose_free_model("این موضوع را تحلیل کن", models) == "deepseek/deepseek-r1:free"
