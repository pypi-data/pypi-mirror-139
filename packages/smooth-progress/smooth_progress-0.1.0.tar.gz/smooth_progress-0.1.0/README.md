# smooth-progress

A simple progress bar made primarily for my own personal use. Was made out of a combination of necessity and being so lazy that I overflowed into being productive and instead of searching for a library that suited my needs, I wrote my own.

## Installation

smooth-progress can be installed through pip. Either download the latest release from Codeberg/GitHub, or do `pip install smooth-progress` to install from PyPi. For the latest commits, check the `dev` branches on the repositories.

smooth-progress was written in Python 3.9, but should work with Python 3.5 and up. A minimum of 3.5 is required due to the project's use of type hinting, which was introduced in that version.

## Usage

Usage of smooth-progress is, as it should be, quite simple.

The driving force of this module is the concept of "mutability", e.g., the openness of the progress bar to change. When the progress bar is mutable, or "open", it can be changed. When it is "closed" it cannot be changed, and will simply display its last state.

The `ProgressBar` model has four basic functions provided for your use:

- `ProgressBar.close()`; closes the ProgressBar from mutability, displaying its final state.
- `ProgressBar.increment()`; progresses the ProgressBar by 1. Should be called once per unit of whatever the bar is measuring.
- `ProgressBar.interrupt()`; a more forceful version of `.close()`, closing the ProgressBar from mutability but without displaying its final state.
- `ProgressBar.open()`; resets the ProgressBar and opens it to mutability.

In the near future, the plans are for `.close()` and `.open()` to be like pause and unpause functions, with `.interrupt()` ending the bar early and `.reset()` resetting its progress.

Here is a simple example to show how the bar is initialised and used:

```
import smooth_progress

bar = simple_progress.ProgressBar(limit=100)
bar.open()
for i in range(0,100):
    bar.increment()
bar.close()
```

Note that the bar is not automatically opened. This is to prevent accidental changes to it if it is initialised before it should be used. In the future, capabilities will be in place to make the above code a little more succinct.

smooth_progress currently also defines one exception, `smooth_progress.exceptions.ProgressBarClosedException`, 
 which is thrown if you attempt to increment the ProgressBar when it is not open.

## Contributing

See [the contribution guide](https://codeberg.org/MurdoMaclachlan/smooth_progress/wiki/Contribution-Guide).