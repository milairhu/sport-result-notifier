# Sport Results and Events Notifier

A Python script that triggers audio notifications for sport results and events. It uses the [api.sportradar.us](https://developer.sportradar.com) API to get live sport events summaries.

## Description

This project is designed to provide real-time notifications for sports events. Currently, it supports Football events, although it can be easily extended to support other sports by mimicking the structure of the Football functions.

The script calls the Sportradar API to get live summaries of the events every minute during a game, each 5 minutes when halftime. When a **goal is scored** or the **game ends**, the script triggers an audio notification. Audio notifications are stored in the [audio](./audio) folder.

## Requirements

No special dependencies requirements are needed to run this script.

However, API keys token are needed for each sport the application might supprot. Keys are findable for free on [api.sportradar.us](https://developer.sportradar.com).

Keys must be stored in a **.env** file in the root of the project. The file should look like this:

```env
MMA_API_KEY={YOUR_MMA_API_KEY}
FOOTBALL_API_KEY={YOUR_FOOTBALL_API_KEY}
```

## Usage

1. Before running the script, make sure to have the **.env** file with the API keys in the root of the project.
2. In your environment, install the required packages by running the following command:

```bash
    pip install -r requirements.txt
```

3. In **main.py**, for using the existing functions for football games, select the team you want to get the notifications for.

An error might be raised in several cases:

- the provided team has no game scheduled in the next minutes and is not currently playing.
- the provided team ended a game too long ago.
- the provided team is not supported by the API. Make sure you use the same name as the one used in the API.

4. To run the script, simply execute the following command:

```bash
    python main.py
```

## Future improvements

- Make the MMA events notifications work.
- Add support for other sports.
- Chose better sound effects
