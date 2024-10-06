const fs = require("fs");

// Class to handle the file processing
class UniqueInt {
  // Method to process the input file and write the output file
  static processFile(inputFilePath, outputFilePath) {
    // Read the file data
    const data = fs.readFileSync(inputFilePath, "utf-8");

    // Call helper function to process the file data
    const uniqueSortedInts = this.processData(data);

    // Write the unique, sorted integers to the output file
    fs.writeFileSync(outputFilePath, uniqueSortedInts.join("\n"), "utf-8");
  }

  // Method to process the data of the file
  static processData(data) {
    const seen = {}; // structure to track seen integers
    const uniqueIntegers = []; // Store unique integers

    // Split the file data by lines
    const lines = data.split("\n");

    for (const line of lines) {
      const trimmedLine = line.trim();

      // Skip empty lines or lines with invalid input
      if (trimmedLine === "") continue;

      // Check if the line contains exactly one integer
      const inputs = trimmedLine.split(/\s+/);
      if (inputs.length !== 1) continue;

      const input = inputs[0];

      // Check if the input is a valid integer
      if (!this.isInteger(input)) continue;

      const number = parseInt(input, 10);

      // If the integer is within the allowed range and hasn't been seen before
      if (number >= -1023 && number <= 1023 && !seen[number]) {
        seen[number] = true; // Mark the integer as seen using an object key
        uniqueIntegers.push(number); // Add to the list of unique integers
      }
    }

    // Manually sort the unique integers in increasing order
    return this.selectionSort(uniqueIntegers);
  }

  // Helper function to check if a string is a valid integer
  static isInteger(str) {
    const num = Number(str);
    return Number.isInteger(num);
  }

  // Manual sorting function
  static selectionSort(arr) {
    for (let i = 0; i < arr.length; i++) {
      let minIndex = i; // Assume the current element is the minimum
      // Find the index of the minimum element in the unsorted portion of the array
      for (let j = i + 1; j < arr.length; j++) {
        // If the current element is smaller than the minimum, update minIndex
        if (arr[j] < arr[minIndex]) {
          minIndex = j;
        }
      }

      // If the minimum element was found, swap it with the current element
      if (minIndex !== i) {
        // Swap elements
        const temp = arr[i];
        arr[i] = arr[minIndex];
        arr[minIndex] = temp;
      }
    }
    return arr;
  }
}

UniqueInt.processFile(
  "../../sample_inputs/sample_input_01.txt",
  "../../sample_results/sample_input_01.txt_results.txt"
);
