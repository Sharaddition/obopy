from search import Brave
from ai import ai
import time

start = time.time()
brave = Brave(api_key='BSAq6KpdUOaCt3PRYEDiPddAborekiX')
q = 'when is sbi releasing electoral bonds list'
res = brave.search(query=q)
if 'altered' in res['query']:
    q = res['query']['altered']
# print(res)
search = ""

keys = ['news', 'videos', 'web']
max_sz = 2200

for key_type in keys:
    if key_type in res:
        for result in res[key_type]['results']:
            if max_sz > len(search):
                search += '\nSource: ' + result['meta_url']['netloc']
                search += '\nTitle: ' + result['title'] + '\n'
                if 'extra_snippets' in result:
                    search += 'Content: ' + ''.join(result['extra_snippets'][0:2]) + '\n'
        break

print('\nSEARCH TIME:', time.time() - start)
ai_start = time.time()
# for result in res['web']['results']:
#     search += '\nSource: ' + result['profile']['name'] + '\n'
#     search += 'Content: ' + ''.join(result['extra_snippets']) + '\n'
# print(search)

prompt = f"""QUERY:

{q}

CONTEXT:
{search}

ANSWER:

"""

# print(prompt)
# print('\n*********************\n')
answer = ai(prompt)
print(answer)

print('\nAI TIME    :',time.time() - ai_start)
print('TOTAL TIME :',time.time() - start)