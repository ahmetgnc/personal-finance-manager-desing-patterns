# Purpose of this Folder

This folder should contain the scaffolded project files to get a student started on their project. This repo will be added to the Classroom for students to use, so please do not have any solutions in this folder.

## Design Reflection

The four patterns cover different parts of the transaction flow:

- **Singleton:** `Balance.get_instance()` provides one shared balance. Direct construction is blocked so different parts of the application cannot accidentally maintain separate totals. Shared state needs care in tests: `reset()` clears both the amount and registered observers.
- **Adapter:** `TransactionAdapter` converts `ExternalFreelanceIncome` into an income `Transaction`. The balance only handles internal transactions, so it does not need to know about invoice IDs or the external platform's fields.
- **Observer:** `Balance` sends the updated amount and transaction to registered observers after each successful transaction. Printing and low-balance alerts stay in their own classes. The alert prints when the balance first falls below the threshold and can trigger again after the balance recovers.
- **Strategy:** `IncomeStrategy` and `ExpenseStrategy` share a `calculate()` interface. `Balance` selects a strategy by category and uses its result before notifying observers. A new calculation rule can be added as another strategy and registered in the category mapping. For two simple operations this adds some structure, but it gives calculation rules a separate place to grow.

The tests cover each part and the complete application flow, including repeated runs, invalid categories, threshold boundaries, and observer removal. The application keeps its state in memory and uses floats for amounts. Persistence and decimal arithmetic would be useful next steps for a larger version.
