import requests as rq
import json
import time


def getting_the_live_data():
    url = "https://api.upstox.com/v3/historical-candle/intraday/NSE_INDEX%7CNifty%2050/minutes/5"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": ""
    }

    response = rq.get(url, headers=headers)
    main_data = response.json()

    with open(
        r"C:\Users\dasho\live_data_rsi_versed.json",
        "w"
    ) as x:
        json.dump(main_data, x, indent=4)

    return main_data


def chroning_the_data(main_data):
    candle_data = main_data["data"]["candles"]

    historical_data = []

    for datas in candle_data:
        data_to_save = {
            "OPEN": datas[1],
            "HIGH": datas[2],
            "LOW": datas[3],
            "CLOSE": datas[4],
            "DATE": datas[0][:10],
            "TIME": datas[0][11:16]
        }

        historical_data.append(data_to_save)

    try:
        with open(
            r"C:\Users\dasho\revised_dataset_rsi_pro_data.json",
            "r"
        ) as x:
            old_data = json.load(x)

    except:
        old_data = []

    existing_times = {
        (x["DATE"], x["TIME"])
        for x in old_data
    }

    for candle in historical_data:
        key = (
            candle["DATE"],
            candle["TIME"]
        )

        if key not in existing_times:
            old_data.append(candle)
            existing_times.add(key)

            print(
                "NEW CANDLE ADDED :",
                candle["DATE"],
                candle["TIME"]
            )

    old_data.sort(
        key=lambda x: (
            x["DATE"],
            x["TIME"]
        )
    )

    with open(
        r"C:\Users\dasho\revised_dataset_rsi_pro_data.json",
        "w"
    ) as x:
        json.dump(
            old_data,
            x,
            indent=4
        )


class RSI_ENGINE:

    def opening_the_raw_data_for_rsi(self):
        with open(
            r"C:\Users\dasho\revised_dataset_rsi_pro_data.json",
            "r"
        ) as x:
            data = json.load(x)

        return data

    def calculating_the_rsi(self):
        rsi_raw_data = self.opening_the_raw_data_for_rsi()

        original_closing_prices = []
        negative_set = []
        positive_set = []

        rsi_data_list = []

        for datas in rsi_raw_data:
            closing_prices = datas["CLOSE"]
            original_closing_prices.append(closing_prices)

        i = 0
        i_data = []
        i2_data = []

        first_element_set = []
        second_element_set = []

        while i < len(original_closing_prices):
            i = i + 1

            if i < len(original_closing_prices):
                i_data.append(i)
                i2_data.append(i - 1)

        for elements in i_data:
            first_element = original_closing_prices[elements]
            first_element_set.append(first_element)

        for seiko in i2_data:
            second_element = original_closing_prices[seiko]
            second_element_set.append(second_element)

        consecutive_difference = [
            x - y
            for x, y in zip(first_element_set, second_element_set)
        ]

        consecutive_14 = consecutive_difference[:14]

        for cons in consecutive_14:
            if cons > 0:
                positive_set.append(cons)

            if cons <= 0:
                positive_set.append(0)

            if cons >= 0:
                negative_set.append(0)

            if cons < 0:
                negative_set.append(abs(cons))

        avg_gain = sum(positive_set) / 14
        avg_loss = sum(negative_set) / 14

        rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))

        rsi_raw_data[14]["RSI"] = rsi

        with open(
            r"C:\Users\dasho\revised_dataset_rsi_pro_data.json",
            "w"
        ) as k:
            json.dump(
                rsi_raw_data,
                k,
                indent=4
            )

        origin_candle = consecutive_difference[14:]

        current_index = 15

        for new_candles in origin_candle:

            if new_candles > 0:
                avg_gain = (
                    (avg_gain * 13) + new_candles
                ) / 14

                avg_loss = (
                    (avg_loss * 13) + 0
                ) / 14

            if new_candles <= 0:
                avg_gain = (
                    (avg_gain * 13) + 0
                ) / 14

                avg_loss = (
                    (avg_loss * 13) + abs(new_candles)
                ) / 14

            rs = avg_gain / avg_loss

            rsi = 100 - (100 / (1 + rs))

            rsi_data_list.append(rsi)

            rsi_raw_data[current_index]["RSI"] = rsi

            current_index += 1

        with open(
            r"C:\Users\dasho\revised_dataset_rsi_pro_data.json",
            "w"
        ) as k:
            json.dump(
                rsi_raw_data,
                k,
                indent=4
            )
while True:
  c=RSI_ENGINE()
  c.opening_the_raw_data_for_rsi()
  c.calculating_the_rsi()


