Anthropic Documents

Getting started
Accessing the API
The API is made available via our web Console. You can use the Workbench to try out the API in the browser and then generate API keys in Account Settings.

Authentication
All requests to the Anthropic API must include an x-api-key header with your API key. If you are using the Client SDKs, you will set the API when constructing a client, and then the SDK will send the header on your behalf with every request. If integrating directly with the API, you'll need to send this header yourself.

Shell

curl https://api.anthropic.com/v1/messages --header "x-api-key: YOUR_API_KEY" ...
Content types
The Anthropic API always accepts JSON in request bodies and returns JSON in response bodies. You will need to send the content-type: application/json header in requests. If you are using the Client SDKs, this will be taken care of automatically.

IP addresses
Anthropic services live at a fixed range of IP addresses. You can add these to your firewall to open the minimum amount of surface area for egress traffic when accessing the Anthropic API and Console. These ranges will not change without notice.

IPv4
160.79.104.0/23

IPv6
2607:6bc0::/48

Versions
When making API requests, you must send an anthropic-version request header. For example, anthropic-version: 2023-06-01. If you are using our client libraries, this is handled for you automatically.

For any given API version, we will preserve:

Existing input parameters
Existing output parameters
However, we may do the following:

Add additional optional inputs
Add additional values to the output
Change conditions for specific error types
Add new variants to enum-like output values (for example, streaming event types)
Generally, if you are using the API as documented in this reference, we will not break your usage.

Version history
We always recommend using the latest API version whenever possible. Previous versions are considered deprecated and may be unavailable for new users.

2023-06-01
New format for streaming server-sent events (SSE):
Completions are incremental. For example, " Hello", " my", " name", " is", " Claude." instead of " Hello", " Hello my", " Hello my name", " Hello my name is", " Hello my name is Claude.".
All events are named events, rather than data-only events.
Removed unnecessary data: [DONE] event.
Removed legacy exception and truncated values in responses.
2023-01-01: Initial release.

Errors
    HTTP errors
        The API follows a predictable HTTP error code format:

        400 - invalid_request_error: There was an issue with the format or content of your request.
        401 - authentication_error: There's an issue with your API key.
        403 - permission_error: Your API key does not have permission to use the specified resource.
        404 - not_found_error: The requested resource was not found.
        429 - rate_limit_error: Your account has hit a rate limit.
        500 - api_error: An unexpected error has occurred internal to Anthropic's systems.
        529 - overloaded_error: Anthropic's API is temporarily overloaded.
        When receiving a streaming response via SSE, it's possible that an error can occur after returning a 200 response, in which case error handling wouldn't follow these standard mechanisms.

    Error shapes
        Errors are always returned as JSON, with a top-level error object that always includes a type and message value. For example:

            JSON

                {
                "type": "error",
                "error": {
                    "type": "not_found_error",
                    "message": "The requested resource could not be found."
                }
                }
        In accordance with our versioning policy, we may expand the values within these objects, and it is possible that the type values will grow over time.

Usage limits:
    To mitigate against misuse and manage capacity on our API, we have implemented limits on how much an organization can use the Claude API.

        There are two types of limits:

            Usage and Rate:
                Usage limits set a maximum monthly cost an organization can incur for API usage
                Rate limits restrict the number of API requests an organization can make over a defined period of time.
                About our limits
                Limits are designed to prevent API abuse, while minimizing impact on common customer usage patterns.
                Limits are defined by usage tier, where each tier is associated with a different set of usage and rate limits.
                Your organization will increase tiers automatically as you reach certain thresholds while using the API.
                Limits are set at the organization level. You can see your organization’s limits in Plans and Billing in the Console.
                You may hit rate limits over shorter time intervals. For instance, a rate of 60 requests per minute (RPM) may be enforced as 1 request per second. Short bursts of requests at a high volume can surpass the rate limit and result in rate limit errors.
                The limits outlined below are our standard limits and apply to the “Build” API plan. If you’re seeking higher, custom limits, contact sales to move to our custom “Scale” plan.
                All Claude models currently have the same usage and rate limits.

            Usage limits

                Each usage tier has a limit on how much you can use the API each calendar month. Once you reach the usage limit of your tier, until you qualify for the next tier, you will have to wait until the next month to be able to use the API again.

                To qualify for the next tier, you must meet a deposit requirement and a mandatory wait period. Higher tiers require longer wait periods. Note, to minimize the risk of overfunding your account, you cannot deposit more than your monthly usage limit.

                    Usage tier	Requirements to advance to tier	Max usage per month
                    Credit purchase	Wait after first purchase
                        Free	        N/A	    0 days	    $10
                        Build Tier 1	$5	    0 days	    $100
                        Build Tier 2	$40	    7 days	    $500
                        Build Tier 3	$200	7 days	    $1,000
                        Build Tier 4	$400	14 days	    $5,000
                        Scale	        N/A	    N/A	        N/A

            Rate limits

                Our rate limits are currently measured in requests per minute, tokens per minute, and tokens per day. If you exceed any of the rate limits you will get a 429 error.

                    Usage tier	Requests per minute (RPM)	Tokens per minute (TPM)	Tokens per day (TPD)
                    Free	            5	                 25,000	                 300,000
                    Build Tier 1	    50	                 50,000	                 1,000,000
                    Build Tier 2	    1,000	             100,000	             2,500,000
                    Build Tier 3	    2,000	             200,000	             5,000,000
                    Build Tier 4	    4,000	             400,000	             10,000,000
                    Scale	            Custom	             Custom	                 Custom

Client Python SDK to work with the Anthropic API. 

Python
Python library GitHub repo

Example:

Python

import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="my_api_key",
)
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    metadata= Metadata (optional),
    stop_sequences= List[str] (optional),
    system= "system_prompt" [str] (optional),
    temperature= [float] (optional),
    top_k= [int] (optional),
    top_p= [float] (optional),
    user_id= [int]/[UUID] (optional),
    stream: [bool] (optional),
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ],
    or for image injection (supported media types=`image/jpeg`,`image/png`, `image/gif`, and `image/webp`),
    messages=[
        {
            "role": "user",
            "content": [
                {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": "/9j/4AAQSkZJRg..."
                }
                },
                { "type": "text", "text": "What is in this image?" }
            ]
            }
    ]        
)
print(message.content)

max_tokens: Required[int]
    """The maximum number of tokens to generate before stopping.

    Note that our models may stop _before_ reaching this maximum. This parameter
    only specifies the absolute maximum number of tokens to generate.

    Different models have different maximum values for this parameter. See
    [models](https://docs.anthropic.com/claude/docs/models-overview) for details.
    """

messages: Required(json[str])
    """Input messages.

    Our models are trained to operate on alternating `user` and `assistant`
    conversational turns. When creating a new `Message`, you specify the prior
    conversational turns with the `messages` parameter, and the model then generates
    the next `Message` in the conversation.

    Each input message must be an object with a `role` and `content`. You can
    specify a single `user`-role message, or you can include multiple `user` and
    `assistant` messages. The first message must always use the `user` role.

    If the final message uses the `assistant` role, the response content will
    continue immediately from the content in that message. This can be used to
    constrain part of the model's response.

    Example with a single `user` message:

        ```json
        [{ "role": "user", "content": "Hello, Claude" }]
        ```

    Example with multiple conversational turns:

        ```json
        [
        { "role": "user", "content": "Hello there." },
        { "role": "assistant", "content": "Hi, I'm Claude. How can I help you?" },
        { "role": "user", "content": "Can you explain LLMs in plain English?" }
        ]
        ```

    Example with a partially-filled response from Claude:

        ```json
        [
        {
            "role": "user",
            "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"
        },
        { "role": "assistant", "content": "The best answer is (" }
        ]
        ```

    Each input message `content` may be either a single `string` or an array of
    content blocks, where each block has a specific `type`. Using a `string` for
    `content` is shorthand for an array of one content block of type `"text"`. The
    following input messages are equivalent:

        ```json
        { "role": "user", "content": "Hello, Claude" }
        ```

        ```json
        { "role": "user", "content": [{ "type": "text", "text": "Hello, Claude" }] }
        ```

    Claude 3 models can send image content blocks:

        ```json
        {
        "role": "user",
        "content": [
            {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": "/9j/4AAQSkZJRg..."
            }
            },
            { "type": "text", "text": "What is in this image?" }
        ]
        }
        ```

    We currently support the `base64` source type for images, and the `image/jpeg`,
    `image/png`, `image/gif`, and `image/webp` media types.

    See [examples](https://docs.anthropic.com/claude/reference/messages-examples)
    for more input examples.

    Note that if you want to include a
    [system prompt](https://docs.anthropic.com/claude/docs/system-prompts), you can
    use the top-level `system` parameter — there is no `"system"` role for input
    messages in the Messages API.
    """

model: Required[
                "claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-2.1'", "claude-2.0", "claude-instant-1.2"
            ]        
    """The model that will complete your prompt.

    See [models](https://docs.anthropic.com/claude/docs/models-overview) for
    additional details and options.
    """

metadata: Metadata
    """An object describing metadata about the request."""

stop_sequences: List[str]
    """Custom text sequences that will cause the model to stop generating.

    Our models will normally stop when they have naturally completed their turn,
    which will result in a response `stop_reason` of `"end_turn"`.

    If you want the model to stop generating when it encounters custom strings of
    text, you can use the `stop_sequences` parameter. If the model encounters one of
    the custom sequences, the response `stop_reason` value will be `"stop_sequence"`
    and the response `stop_sequence` value will contain the matched stop sequence.
    """

system: str
    """System prompt.

    A system prompt is a way of providing context and instructions to Claude, such
    as specifying a particular goal or role. See our
    [guide to system prompts](https://docs.anthropic.com/claude/docs/system-prompts).
    """

temperature: float
    """Amount of randomness injected into the response.

    Defaults to `1.0`. Ranges from `0.0` to `1.0`. Use `temperature` closer to `0.0`
    for analytical / multiple choice, and closer to `1.0` for creative and
    generative tasks.

    Note that even with `temperature` of `0.0`, the results will not be fully
    deterministic.
    """

top_k: int
    """Only sample from the top K options for each subsequent token.

    Used to remove "long tail" low probability responses.
    [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

    Recommended for advanced use cases only. You usually only need to use
    `temperature`.
    """

top_p: float
    """Use nucleus sampling.

    In nucleus sampling, we compute the cumulative distribution over all the options
    for each subsequent token in decreasing probability order and cut it off once it
    reaches a particular probability specified by `top_p`. You should either alter
    `temperature` or `top_p`, but not both.

    Recommended for advanced use cases only. You usually only need to use
    `temperature`.
    """

user_id: Optional
    """An external identifier for the user who is associated with the request.

    This should be a uuid, hash value, or other opaque identifier. Anthropic may use
    this id to help detect abuse. Do not include any identifying information such as
    name, email address, or phone number.
    """

stream: Optional
    """Whether to incrementally stream the response using server-sent events.

    See [streaming](https://docs.anthropic.com/claude/reference/messages-streaming)
    for details.
    """
