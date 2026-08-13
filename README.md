# Currency Converter

A modern Currency Converter web application built using Python and Streamlit. The application allows users to convert currencies using exchange-rate API data, swap currencies instantly, and view exchange rates through a clean and responsive interface.

## Project Overview

This project provides a simple and user-friendly currency conversion experience. Users can select a source currency, choose a target currency, enter an amount, and instantly view the converted amount along with the current exchange rate.

## Features

* Convert between multiple international currencies
* Exchange-rate data from an API
* Swap source and target currencies
* Real-time amount conversion
* Currency flags for visual identification
* Responsive Streamlit interface
* Sidebar-based conversion controls
* Fast and lightweight application

## Technologies Used

* Python 3
* Streamlit
* Requests
* HTML
* CSS
* Exchange Rate API

## Project Structure

```text
currency-converter-streamlit/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
├── README.md              # Project documentation
│
├── assets/
│   └── style.css          # Custom styling
│
└── templates/
    └── index.html         # Header template
```

## Installation

### Clone the repository

```bash
git clone https://github.com/your-username/currency-converter-streamlit.git
```

### Navigate to the project folder

```bash
cd currency-converter-streamlit
```

### Install the required packages

```bash
pip install -r requirements.txt
```

### Run the application

```bash
streamlit run app.py
```

## Usage

1. Open the Streamlit application in your browser.
2. Select the **From Currency**.
3. Select the **To Currency**.
4. Enter the amount you want to convert.
5. Click **Convert Now**.
6. View the converted amount and exchange rate.
7. Use **Swap Currencies** to exchange the selected currencies instantly.

## Requirements

* Python 3.9 or higher
* Streamlit
* Requests

## Future Improvements

* Historical exchange-rate charts
* Currency trend graphs
* Favorite currency pairs
* Offline conversion support
* Dark and light mode toggle
* Multi-language support

## Contributing

Contributions are welcome. Feel free to fork the repository, create a new branch, and submit a pull request.

## License

This project is licensed under the MIT License.

## Author

**Bhargav Bhoge**

If you found this project useful, consider giving it a star on GitHub.
