# Smart Keyrack Build

Source code for smart key rack that is run on a raspberry pi zero

## Installation

Install dotenv 

```bash
sudo -H pip3 install -U python-dotenv
```

Copy `env-sample` to `.env` and then edit the `.env` file

Add the `IFTTT_WEBHOOK_KEY` value to the `.env` file.  The value can be retrieved by clicking on the `Documentation` link on the [IFTTT Webhooks page](https://ifttt.com/maker_webhooks).


## Resources

- [Installing NeoPixel on a pi](https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage)
