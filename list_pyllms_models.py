import llms

model=llms.init()
models = model.list()
providers = []
for model in models:
    provider = model["provider"]
    provider = provider.replace("Provider", "").lower()
    providers.append(f'{provider}_{model["name"]}')
providers.sort()
for provider in providers:
    print(provider)