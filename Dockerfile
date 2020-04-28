FROM python:3
ADD bot.py /
ADD log.py /
RUN python3 -m pip install -U discord.py
RUN python3 -m pip install ping3
RUN python3 pip install python-dotenv
CMD [ "python", "./bot.py" ]

