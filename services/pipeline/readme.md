# augment

## testing after code change

set temp vars in main fct
docker compose run --rm augmentation python main.py

## work steps

1) sys prompts
2) example chunks
3) kick off tavily
4) helpers for local vs api llm
5) check if chunks are suff for response
6) parse outputs
7) main orchestration

## schnittstellen

inputs:

- frontend: query, style (tech, creative, defensive teomplate), resp length (max token), mode local/api
- reranker: top k chunks

output:

- response as string to frontend

## timers

added timers for eval: -> total = eval + fetch + generation

## stuff for future?

- different local llms: small, medium, big (choose frontend)
- maybe add feature for resp length? small, medium, big // character brackets

- prompt compression (if generation time too big) -> timeout gen > 60s, maybe compress context

- prompt caching (dont see it now)
- prompt chaining: idk ... kinda did already with tavily
- reranker: out of scope, part of retrieval?

- error handling if no answer from local/api/tavily
