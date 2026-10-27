# Personal Finance Manager — Design Patterns Project

This project is a hands-on exercise in applying Object-Oriented Design Patterns to build a simplified personal finance manager.
You will implement and extend starter code to add functionality such as tracking transactions, adapting external data, observing balance changes, and ensuring proper architectural patterns.

## Getting Started

### Dependencies

Make sure you have python version >= 3.10.x installed on your computer. 


### Installation

1. Clone the repo:

```
bash
git clone https://github.com/udacity/cd14600-project-starter.git
cd cd14600-project-starter/starter
```

2. Run the Program: 
```
python main.py
```

## Testing

This project uses Python’s built-in unittest framework.

To run all tests from the `starter` directory:

```
python -m unittest discover
```

From the repository root, use:

```
python -m unittest discover -s starter
```

To run a single test file from the `starter` directory:
```
python -m unittest balance/test_balance_observer.py
```

### Break Down Tests

- test_balance.py → Checks Singleton behavior, transaction handling, and strategy selection.
- test_transaction.py → Checks transaction creation, string output, and equality.
- test_transaction_adapter.py → Ensures external income data is correctly adapted into Transaction objects.
- test_balance_observer.py → Validates that low-balance alerts are triggered at the correct threshold.
- test_main.py → Checks the complete transaction flow and repeated application runs.

## Project Instructions

1. Implement Singleton Balance Class – Ensure only one balance object exists throughout the app.
2. Complete Transaction Class – Handle income and expense transactions.
3. Implement Adapter Pattern – Adapt external freelance income data into internal Transaction objects.
4. Implement Observer Pattern – Create a low balance observer that triggers an alert when funds drop too low.
5. Add Unit Tests – Write tests for all implemented functionality.
6. Choose and Implement a Fourth Pattern – Pick one additional design pattern (e.g., Strategy, Command, Decorator, etc.) and integrate it into your project.
7. Provide a Reflection – Add a short write-up in your repo (README or separate file) explaining your design choices.

## Design Reflection

The four patterns cover different parts of the transaction flow:

- **Singleton:** `Balance.get_instance()` provides one shared balance. Direct construction is blocked so different parts of the application cannot accidentally maintain separate totals. Shared state needs care in tests: `reset()` clears both the amount and registered observers.
- **Adapter:** `TransactionAdapter` converts `ExternalFreelanceIncome` into an income `Transaction`. The balance only handles internal transactions, so it does not need to know about invoice IDs or the external platform's fields.
- **Observer:** `Balance` sends the updated amount and transaction to registered observers after each successful transaction. Printing and low-balance alerts stay in their own classes. The alert prints when the balance first falls below the threshold and can trigger again after the balance recovers.
- **Strategy:** `IncomeStrategy` and `ExpenseStrategy` share a `calculate()` interface. `Balance` selects a strategy by category and uses its result before notifying observers. A new calculation rule can be added as another strategy and registered in the category mapping. For two simple operations this adds some structure, but it gives calculation rules a separate place to grow.

The tests cover each part and the complete application flow, including repeated runs, invalid categories, threshold boundaries, and observer removal. The application keeps its state in memory and uses floats for amounts. Persistence and decimal arithmetic would be useful next steps for a larger version.

## Built With

* [Python](https://www.python.org/) – Main programming language
* [unittest](https://docs.python.org/3/library/unittest.html) – Testing framework
* [PEP8](https://peps.python.org/pep-0008/) – Style guide for Python code

## License

[License](LICENSE.txt)
