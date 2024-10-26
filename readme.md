# Prayer Times Calendar Generator

This script generates an `.ics` calendar file with prayer times for a specified date range and location. It uses the `praytimes` library to calculate prayer times and allows customization of prayer durations.

## Features

- Calculates prayer times for any location based on latitude and longitude.
- Uses the `Karachi` calculation method by default, but can be easily modified to use other methods (MWL, ISNA, Egypt, Makkah, Tehran, Jafri).
- Uses the `Hanafi` school of thought for Asr prayer calculation by default, but can be changed to `Standard`.
- Allows customization of prayer durations, with a separate option for Dhuhr prayer.
- Generates an `.ics` file that can be imported into any calendar application.

## Requirements

- Python 3.6 or higher
- `praytimes` package
- `ics` package
- `pandas` package

You can install the required packages using `pip`:

```bash
pip install -r requirements.txt