import sys

class SparseMatrix:
    def __init__(self, rows=None, cols=None):
        self.numRows = rows
        self.numCols = cols
        self.elements = {}  # dictionary to store non-zero elements (rows, col): value

    @staticmethod
    def from_file(matrixFilePath):
        """ Read the file to extract the matrix structure """
        matrix = SparseMatrix()
        with open(matrixFilePath, 'r') as f:
            lines = f.readlines()
            matrix.numRows = int(lines[0].split('=')[1])
            matrix.numCols = int(lines[1].split('=')[1])

            for line in lines[2:]:
                line = line.strip()
                if not line or not line.startswith('(')     :
                    print(f"Input file has wrong format.")
                    sys.exit()
                try:
                    row, col, value = map(int, line.strip('()').split(','))
                    matrix.set_element(row, col, value)
                except ValueError:
                    raise ValueError("Input file has wrong format")
        return matrix

    def set_element(self, row, col, value):
        """ Set the value in the matrix if the value is not zero """
        try:
            if row >= self.numRows or col >= self.numCols:
                print(f"Warning: Index ({row}, {col}) is out of bounds. Skipping this entry.")
            if value != 0:
                self.elements[(row, col)] = value
        except Exception as e:
            print(f"An error occurred while setting the element: {e}")

    def get_element(self, row, col):
        """ Retrieves the value at a given row and column """
        return self.elements.get((row, col), 0)

    def add(self, other):
        """ Add two sparse matrices """
        if self.numRows != other.numRows or self.numCols != other.numCols:
            print("Matrix dimensions do not match for addition.")
            return None

        result = SparseMatrix(self.numRows, self.numCols)
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value + other.get_element(row, col))
        for (row, col), value in other.elements.items():
            result.set_element(row, col, value)
        return result

    def subtract(self, other):
        """ Subtract two sparse matrices """
        if self.numRows != other.numRows or self.numCols != other.numCols:
            print("Matrix dimensions do not match for subtraction.")
            return None

        result = SparseMatrix(self.numRows, self.numCols)
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value - other.get_element(row, col))
        for (row, col), value in other.elements.items():
            if (row, col) not in self.elements:
                result.set_element(row, col, -value)
        return result

    def multiply(self, other):
        """ Multiply two sparse matrices """
        if self.numCols != other.numRows:
            print("Matrix dimensions do not match for multiplication.")
            return None

        result = SparseMatrix(self.numRows, other.numCols)
        for (row1, col1), value1 in self.elements.items():
            for col2 in range(other.numCols):
                value2 = other.get_element(col1, col2)
                if value2 != 0:
                    current_val = result.get_element(row1, col2)
                    result.set_element(row1, col2, current_val + value1 * value2)
        return result

    def to_file(self, filePath):
        """ Writes the result of an operation of the sparse matrix to the specified file """
        try:
            with open(filePath, 'w') as f:
                f.write(f"rows={self.numRows}\n")
                f.write(f"cols={self.numCols}\n")
                for (row, col), value in sorted(self.elements.items()):
                    f.write(f"({row},{col},{value})\n")
            print(f"Results written to {filePath}")
        except Exception as e:
            print(f"An error occurred while writing to file: {e}")

def main():
    try:
        matrixA = SparseMatrix.from_file('../../sample_inputs/easy_sample_01_2.txt')
        matrixB = SparseMatrix.from_file('../../sample_inputs/easy_sample_01_3.txt')
        result_path = '../../sample_results/results.txt'

        operation = input("Available operations: \n1. add \n2. subtract \n3. multiply \nEnter the number corresponding to the operation to perform: ").strip().lower()

        if operation == '1':
            result = matrixA.add(matrixB)
            if result:
                result.to_file(result_path)
        elif operation == '2':
            result = matrixA.subtract(matrixB)
            if result:
                result.to_file(result_path)
        elif operation == '3':
            result = matrixA.multiply(matrixB)
            if result:
                result.to_file(result_path)
        else:
            print("Invalid operation selected.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
