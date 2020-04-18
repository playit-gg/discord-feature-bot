FROM python:3
ADD bot.py /
ADD discord.key /
RUN pip install -U discord.py
CMD [ "python", "./bot.py" ]

