FROM python:3
ADD bot.py /
ADD discord.key /
ADD log.py /
ADD reaction.txt /
RUN pip install -U discord.py
RUN pip install ping3
CMD [ "python", "./bot.py" ]

