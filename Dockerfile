FROM python:3
ADD bot.py /
ADD discord.key /
ADD log.py /
ADD reaction.txt /
RUN python3 -m pip install -U discord.py
RUN python3 -m pip install ping3
CMD [ "python", "./bot.py" ]

