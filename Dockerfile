FROM python:3
ADD bot.py /
ADD discord.key /
ADD log.py /
ADD reaction.txt /
RUN pip install -U discord.py
CMD [ "python", "./bot.py" ]

