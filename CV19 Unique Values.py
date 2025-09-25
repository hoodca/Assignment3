# Specify the column index (0-based) you want to isolate
column_index = 1  # Example: Second column

# You can change these two settings if needed
file_path = 'usscv19d.csv'
file_encoding = 'utf-8'  # change to e.g. 'cp1252' if you hit a decode error

try:
    # Basic validation for column index
    if not isinstance(column_index, int) or column_index < 0:
        print("Error: column_index must be a non-negative integer.")
        raise SystemExit(1)

    # Open the CSV file
    try:
        with open(file_path, 'r', encoding=file_encoding) as file:
            # Read all lines
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: Input file not found:", file_path)
        raise SystemExit(1)
    except UnicodeDecodeError as e:
        print("Error: Failed to decode file with encoding '", file_encoding, "'.", sep="")
        print("Hint: Update file_encoding at the top of the script to match your file.")
        print("Details:", e)
        raise SystemExit(1)
    except OSError as e:
        print("Error: Could not read the file:", e)
        raise SystemExit(1)

    if not lines:
        print("Error: The file is empty.")
        raise SystemExit(1)

    # Remove header
    header_line = lines[0].strip()
    header = header_line.split(",")
    if column_index >= len(header):
        # Not fatal, as some data rows might have more columns, but warn.
        print(
            "Warning: header has", len(header), "columns; column_index",
            column_index, "may be out of range for the header."
        )
    data_rows = lines[1:]

    # Extract the desired column
    isolated_column = []
    for row_num, line in enumerate(data_rows, start=2):  # start=2 to account for header line
        # Skip completely blank lines
        if not line.strip():
            continue
        # Split the line by commas
        values = line.strip().split(',')
        # Append the value from the desired column, or warn if missing
        if len(values) > column_index:
            isolated_column.append(values[column_index])
        else:
            print(
                "Warning: line", row_num,
                "has only", len(values), "column(s); skipping"
            )

    if not isolated_column:
        print("Error: No data collected for column_index", column_index)
        raise SystemExit(1)

    # Count each unique state abbreviation appearing in the isolated column
    unique_values = {}
    for value in isolated_column:
        if value in unique_values:
            unique_values[value] += 1
        else:
            unique_values[value] = 1

    if not unique_values:
        print("Notice: No unique values found.")
        raise SystemExit(0)

    # Print the count of unique state abbreviations
    for state, count in unique_values.items():
        print(f"{state}: {count}")

except SystemExit:
    # Allow clean exits above to terminate without stack traces
    pass
except Exception as e:
    # Last-resort catch to avoid silent crashes
    print("Unexpected error:", e)
    raise