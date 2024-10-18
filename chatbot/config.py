def create_openai_client():
    from openai import OpenAI
    return OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key="YOUR_OPENAI_API_KEY"
    )

