from os import system
depend = ['nextcord', 'nextcord.ext', 'nextcord.utils', 'flask', 'threading', 'os', 'time', 'json', 'logging', 'dotenv', 'sys']

for dep in depend:
    system(f'python3 -m poetry add {dep}')
