public class Program
{
    public static void Main(string[] args)
    {
        string inputFile = "input.csv";
        string outputFile = "output.csv";

        try
        {
            string[] lines = File.ReadAllLines(inputFile);
            string header = lines[0];
            int totalRows = lines.Length -1;

            int eligibleVoters = 0;

            for(int i = 1; i < lines.Length; i++)
            {
                string[] columns = lines[i].Split(',');
                string name = columns[0];
                int age = int.Parse(columns[1]);
                string city = columns[2];

                if(age >= 18)
                {
                    eligibleVoters++;
                }
            }

            string result = $"CSV Analysis Report\n" +
                $"Total Records : {totalRows}\n" +
                $"Eligible Voters: {eligibleVoters}\n";

                File.WriteAllText(outputFile, result);

                Console.WriteLine($"Results saved to {outputFile}");

        }
        catch (FileNotFoundException)
        {
            Console.WriteLine($"Error: {inputFile} not found.");
        }
        catch (FormatException)
        {
            Console.WriteLine("Error: Invalid format");
        }
        catch (IndexOutOfRangeException)
        {
            Console.WriteLine("Error: Missing columns in csv");
        }
        catch (IOException ex)
        {
            Console.WriteLine($"Error; {ex.Message}");
        }
    }
}