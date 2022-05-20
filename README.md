<h1 align="center">Welcome to Arduino Morse Code Reader 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-blue.svg?cacheSeconds=2592000" />
</p>

> A python tool for reading in button presses from a bread board through an Arduino MicroController. Uses the Firmata protocol to allow python code controlling the Arduino to run on users laptop.


## Dev

### Install
```sh
poetry install
```

### Usage

```sh
poetry run morse [COMMAND]
```

## CLI

### Install
```sh
pip3 install dist/morse-0.1.2-py3-none-any.whl
```

### Usage
```sh
morse
```
Help functions are available to walk you through process

## Full Process
1.) Open the ardunio app
2.) export the StandardFirmata/StandardFirmata.ino to the board
     - If you are having serial port issues try using port: /dev/cu.usbserial-DN01ADTL
3.) make sure morse CLI is installed
4.) type morse at the terminal

## Author

👤 **John Pignato**

* Github: [@jpig18](https://github.com/jpig18)

👤 **Jordan Trombly**

* Github: [@Jordant190](https://github.com/Jordant190)

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_