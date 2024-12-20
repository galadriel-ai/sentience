from openai.types import CompletionUsage
from openai.types.chat import ChatCompletion
from openai.types.chat import ChatCompletionMessage
from openai.types.chat import ChatCompletionMessageToolCall
from openai.types.chat.chat_completion import Choice
from openai.types.chat.chat_completion_message_tool_call import Function

import sentience


def _get_mock_completion() -> ChatCompletion:
    return ChatCompletion(
        id="test_id",
        created=1234567890,
        model="test_model",
        object="chat.completion",
        service_tier=None,
        system_fingerprint="fingerprint",
        usage=CompletionUsage(prompt_tokens=10, completion_tokens=20, total_tokens=30),
        choices=[
            Choice(
                index=0,
                finish_reason="stop",
                message=ChatCompletionMessage(
                    content="hello",
                    role="assistant",
                    tool_calls=[
                        ChatCompletionMessageToolCall(
                            id="test_id",
                            function=Function(arguments="{}", name="test_function"),
                            type="function",
                        )
                    ],
                ),
            )
        ],
    )


def test_empty():
    completion = _get_mock_completion()
    result = sentience.verify_signature(completion)
    assert result is False


def test_invalid_inputs():
    completion = _get_mock_completion()
    completion.public_key = "a"
    completion.hash = "a"
    completion.signature = "a"
    result = sentience.verify_signature(completion)
    assert result is False


def test_invalid_signature():
    completion = _get_mock_completion()
    completion.public_key = (
        "835cc0e84c2a5190561d7c2eaf10eb2597cbe7a71541084c5edea32b60bc5e68"
    )
    completion.hash = "c847e98b1abf528f988c0253840616405a014ef2494e7a1b6c8d35e90413dd0a"
    completion.signature = "18603b802f1e293dbf21bb1004bd08bca272fc70b6d00556f2a06b35949319533ad527c614c063836601aa00c8ca960dc600cad990df1ff8ff18079a09561d07"
    result = sentience.verify_signature(completion)
    assert result is False


def test_invalid_hash():
    completion = _get_mock_completion()
    completion.public_key = (
        "835cc0e84c2a5190561d7c2eaf10eb2597cbe7a71541084c5edea32b60bc5e68"
    )
    completion.hash = "1847e98b1abf528f988c0253840616405a014ef2494e7a1b6c8d35e90413dd0a"
    completion.signature = "68603b802f1e293dbf21bb1004bd08bca272fc70b6d00556f2a06b35949319533ad527c614c063836601aa00c8ca960dc600cad990df1ff8ff18079a09561d07"
    result = sentience.verify_signature(completion)
    assert result is False


def test_invalid_public_key():
    completion = _get_mock_completion()
    completion.public_key = (
        "135cc0e84c2a5190561d7c2eaf10eb2597cbe7a71541084c5edea32b60bc5e68"
    )
    completion.hash = "c847e98b1abf528f988c0253840616405a014ef2494e7a1b6c8d35e90413dd0a"
    completion.signature = "68603b802f1e293dbf21bb1004bd08bca272fc70b6d00556f2a06b35949319533ad527c614c063836601aa00c8ca960dc600cad990df1ff8ff18079a09561d07"
    result = sentience.verify_signature(completion)
    assert result is False


def test_valid():
    completion = _get_mock_completion()
    completion.public_key = (
        "835cc0e84c2a5190561d7c2eaf10eb2597cbe7a71541084c5edea32b60bc5e68"
    )
    completion.hash = "c847e98b1abf528f988c0253840616405a014ef2494e7a1b6c8d35e90413dd0a"
    completion.signature = "68603b802f1e293dbf21bb1004bd08bca272fc70b6d00556f2a06b35949319533ad527c614c063836601aa00c8ca960dc600cad990df1ff8ff18079a09561d07"
    result = sentience.verify_signature(completion)
    assert result is True
