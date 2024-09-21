<div align="center">
<h2>BashGPT: ChatGPT for Command Line</h2>
</div>

A simple command line tool to run ChatGPT. Currently still work in progress.

## Installation
### Debian Package
Currently I provide one pre-built debian package:
```bash
dpkg -i build bashgpt-0.0.1.deb
```
### From Source
```bash
source dev/env.sh
build_tool [version number]
dpkg -i builds/bashgpt-[version number].deb
```

## Usage
The tool can simply be called via command-line:
### Question Answering
```bash
gpt ask [question]
```
### Print Configuration
To see the available configuration parameters and their current value:
```bash
gpt config
```
### Set Configuration
```bash
gpt set [key] [value]
```
## License
`BashGPT` is licensed under BSD-3

## Disclaimer
This project is still work in progress and there is plan to add more functionalities