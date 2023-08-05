# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['throttled', 'throttled.fastapi', 'throttled.storage']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'throttled',
    'version': '0.1.16a38',
    'description': 'A rate limiter for FastAPI',
    'long_description': '# ThrottledAPI\n\nThis repo aims to be an audacious rate limiter for FastAPI. \nCheck [our features](tests/acceptance/features/fastapi_limiter.feature) to see the use-cases already tested.\n\n## Why another rate limiter for FastAPI?\n\nWhy another rate limiter for FastAPI, if we already have \n[slowapi](https://github.com/laurentS/slowapi) and \n[fastapi-limiter](https://github.com/long2ice/fastapi-limiter)? This limiter glues what is good from both projects and \nadds a bit more. Here is a list of reasons:\n\n- The `throttled-api` rate limiter takes full advantage from the composable dependency injection system in FastAPI. \nThat means you can also create limiters per resource.\n    - Want to limit requests per IP or per user? Got it! \n    - Want to limit requests based on another weird parameter you are receiving? Just extend our `FastAPILimiter` and you\nare good to go!\n- You can use different storage storages backends (different implementations for `BaseStorage`) for each limiter.\n    - Want to each API instance to 2000 requests per second? You don´t need more than a *in-memory* counter.\nJust use `MemoryStorage` for the task.\n    - Want to limit calls to all your API instances by user or IP? A shared cache is what you need. \nOur `RedisStorage` implementation is an adapter for the famous `redis` package. Other implementations + asyncio support are comming...\n\n## Instalation\n\nJust use your favorite python package manager. Here are two examples:\n\n- With pip: `pip install throttled`\n- With poetry: `poetry add throttled`\n\n## Usage\n\n```python\n\n```\n\n## Middleware vs Dependency\n\nAlthough FastAPI dependency injection is really powerfull, some limiters doesn´t require any special resource in other to use it.\nIn that case you cut some latency if using the limiter as a Middleware. To do that, just extend our `MiddlewareLimiter`, which is \na extension of `FastAPILimiter` to work as a middleware.\n\n### When implementing a custom limiter, how to choose between extending `FastAPILimiter` or `MiddlewareLimiter`?\n\n```mermaid\nstateDiagram-v2\n    state FirstCondition <<choice>>\n    state SecondCondition <<choice>>\n    \n    FirstQuestion: What type of limiter should I choose?\n    FirstQuestion --> FirstCondition\n    \n    FirstCondition: Limitting depends on resources other\\nthan Request object from Starlette?\n    FirstCondition --> FastAPILimiter: yes\n    FirstCondition --> MiddlewareLimiter : no\n    FastAPILimiter --> SecondQuestion\n    MiddlewareLimiter --> SecondQuestion\n    \n    SecondQuestion: What storage should I pick?\n    SecondQuestion --> SecondCondition\n    SecondCondition: The parameters you are limitting spams a parameter space.\\n Is that space too large?\n    SecondCondition --> RedisStorage : yes\n    SecondCondition --> ThirdCondition : no\n    \n    ThirdCondition: You want to share the limiter\\nbetween different API instances (pods)?\n    ThirdCondition --> RedisStorage : yes\n    ThirdCondition --> MemoryStorage : no\n    \n    RedisStorage --> End\n    MemoryStorage --> End\n    End: Attach the limiter to your API     \n```\n',
    'author': 'Vinícius Vargas',
    'author_email': 'santunionivinicius@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/santunioni/ThrottledAPI',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
