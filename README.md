# kankagen.py

Dirty script to skip 66% of the boring boilerplate of generating NPCs for writing projects.

**Contents**:

- [kankagen.py](#kankagenpy)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)

## Installation

1. `git clone https://github.com/onoira/kankagen && cd kankagen`
2. `touch .env` (see example below)
3. (in your venv of choice) `python3 -m pip install -r requirements.txt`
4. <https://kanka.io/en/docs/1.0/setup>
   - Set `KANKA_API_TOKEN`
   - Set `KANKA_CAMPAIGN_ID` from the campaign URL (`kanka.io/en/campaign/{campaign_id}`)
5. <https://perchance.org/diy-perchance-api>
   - Set `GLITCH_DOMAIN` from your <https://glitch.me> domain (`{domain}.glitch.me`)
6. Set `KANKAGEN_PERCHANCE_GENERATOR_ID` from your <https://perchance.org/> URL (`perchance.org/{generator_id}`; _e.g._ <https://perchance.org/ono-character-background>)

Example `.env`:

    export KANKA_API_TOKEN=""
    export KANKA_CAMPAIGN_ID=""
    export GLITCH_DOMAIN=""
    export KANKAGEN_PERCHANCE_GENERATOR_ID=""

## Usage

    . ./.env
    python gen.py "John Doe" Male

## Contributing

This repository is not open for contributions. Forking is encouraged.

## License

[AGPLv3](LICENSE)
