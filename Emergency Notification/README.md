# Emergency Notification Test

Identify whether an emergency notification has appeared.

Works with screenshots of different devices through OCR.

## Prerequisites

-   **Python**: Tested using version 3.11.8

### Python Modules

-   **pytesseract**: Used for OCR
-   **opencv-python**: Used for image processing

Install using:

```
pip install -r requirements.txt
```

## Usage

```
python emergency_test.py -i <image_path> -w <words_list_path> [options]

Options:
    -c, --min-conf <conf-percent>  Set minimum confidence for text to be accepted. [default: 90]
    -l, --lang <language>          Set language to be processed by OCR. [default: eng]

```

## Result:

-   Prints `Pass` if image passes
-   Prints `Fail` if image fails

## Words list format

-   Each line should contain the entire key phrase to be searched for.
-   The test will only pass if all the text in a line is contained in the image.

Example:

```
National alert
Emergency alert: Extreme
```

## List of languages

https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html
