### Clearing Specific Session Keys After Un/Successful Payment

```python
# Clear specific session keys after un/successful payment
keys_to_delete = ['save_info', 'download_password', ]
for key in keys_to_delete:
    try:
        del request.session[key]
    except KeyError:
        print(f"Key {key} not found in session. Skipping deletion.")
```

#### What Does it Do?
- This code snippet is designed to clear specific keys from the user's session after a successful payment.
  
#### How Does it Work?
1. A list named `keys_to_delete` is defined, containing the keys that should be removed from the session.
2. A `for` loop iterates over each key in this list.
3. Inside the loop, a `try...except` block attempts to delete each key from the session.
4. If the key exists, it will be deleted. If the key does not exist, a `KeyError` exception will be caught, deletion will be skipt, and a message will be printed to the console without breaking the code.

---

### Printing All Items in the Session

It's useful to know the number of keys in the session object at a certain point in our code. This information can help us optimize the performance of the preceding code block.

```python
# Print all items in the session
session = request.session
for item, value in session.items():
    print(f"Session key: {item}, value: {value}")
```

#### What Does it Do?
- This code snippet prints out all the key-value pairs currently stored in the user's session.

#### How Does it Work?
1. The `session` variable is assigned the user's session dictionary.
2. A `for` loop iterates over all key-value pairs in the session.
3. Inside the loop, each key-value pair is printed to the console for debugging or informational purposes.
